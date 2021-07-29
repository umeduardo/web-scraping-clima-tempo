from typing import Dict, List, Any

from bs4 import BeautifulSoup
import requests
from flask import Flask
from flask import Response, request
import json
import re

app = Flask(__name__)

def _sanitize_value(data_type: str, value: str) -> str:
    """
    Return formatted string to each data type.
    """


    if data_type == 'temperatura':
        return "ºC ".join(value.split("°")).strip()
    elif data_type == 'chuva':
        return value.replace("\n","")
    elif data_type == 'vento':
        return value.replace("\n","")
    elif data_type == 'umidade':
        return "% ".join(value.replace("\n","").split("%")).strip()
    elif data_type == 'sol':
        return "h ".join(value.replace("\n","").split("h")).strip()
    else:
        return value.replace("\n","")


@app.route("/previsao", methods=('GET',))
def get_previsao() -> Response:
    """
    Return weather forecast by city id
    eg:
    return {"cidade": "São Paulo - SP", "temperatura": "5ºC 14ºC", "chuva": "0mm -0%", "vento": "SSW-17km/h", "umidade": "13% 73%", "sol": "06:57h 17:58h"}
    """
    id_cidade: str = re.sub('/(^[0-9])/', '', request.args.get('id_cidade',''))
    if id_cidade == '':
        return Response(response="Nada Encontrado", mimetype="text/plain")
    else:
        source: bytes = requests.get(f'https://www.climatempo.com.br/previsao-do-tempo/cidade/{id_cidade}/teresina-pi').content
        soup: BeautifulSoup = BeautifulSoup(source, 'html.parser')

        previsao: BeautifulSoup = soup.find("div", class_="card -no-top -no-bottom")
        variables: List[Any] = previsao.select(".variables-list > li")

        dados: Dict[str, str] = {}
        dados['cidade'] = soup.select("h2", 
            class_="-gray -uppercase -bold -font-small _margin-t-20")[0].get_text(strip=True).replace(
            "Not\u00edcias e Previs\u00e3o do tempo em ","")
        for variable in variables:
            _name: str = variable.select('.variable')[0].get_text(strip=True).lower()
            _value: List[Any] = variable.select('._flex')

            if len(_value) == 0:
                _value = variable.select('span:nth-of-type(2)')

            _value = _sanitize_value(_name, _value[0].get_text(strip=True))
            dados[_name] = _value
            
        return Response(response=json.dumps(dados), mimetype="application/json")


@app.route("/cidades", methods=('GET',))
def get_cidades() -> Response:
    """
    Returns a list of cities containing the {{name}} parameter in the name
    eg:
    return {"cidade": "São Paulo - SP", "temperatura": "5ºC 14ºC", "chuva": "0mm -0%", "vento": "SSW-17km/h", "umidade": "13% 73%", "sol": "06:57h 17:58h"}
    """
    response_json: Any = requests.post('https://www.climatempo.com.br/json/busca-por-nome', {"name":request.args.get('name','')})
    if response_json.status_code == 200:
        
        result_list: Dict = {}

        results: list = json.loads(response_json.content)
        for result_type in results:
            response_json = result_type['response']
            if response_json['success']:
                for city in response_json['data']:
                    result_list[city['idcity']] = {
                            "cidade_id": city['idcity'],
                            "uf": city['uf'],
                            "capital": city.get('capital'),
                            'pais': city.get('country'),
                            "base": city.get('base'),
                        }

        return Response(response=json.dumps(result_list), mimetype="application/json")
    else:
        return Response(response="[]", mimetype="application/json")

