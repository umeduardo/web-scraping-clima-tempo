# web-scraping-clima-tempo
Desenvolvimento de um web scraping para consulta de dados do site ClimaTempo. 


#Instalação

###Instale os pacotes necessários
```1) $ python3.6 -m venv ./env
2) $ pip install -r config/requirements.txt
3) $ source env/bin/activate
```
###Defina as variáveis de ambiente e rode o projeto
```4) $ export FLASK_ENV=development
5) $ export FLASK_APP=main
6) $ cd src && flask run
```


# Métodos
###Consulta de Cidades
- http://127.0.0.1:5000/cidades?name=São%20Paulo

###Consulta de Previsões do Tempo
- http://127.0.0.1:5000/previsao?id_cidade=558
