# app.py
import requests
import logging

from flask import jsonify, redirect
from pydantic import BaseModel
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag

import pickle
from sklearn import svm

#Carregando o modelo de ML exportado a partir do Notebook Colab
endereco_do_modelo = "./modelo_ml/classifier.pkl"
pickle_in = open(endereco_do_modelo, 'rb')
modelo = pickle.load(pickle_in)
pickle_in.close()

#Testando
teste = [1.021, 4.9, 725, 14, 443, 2.45]
predicao = modelo.predict([teste])
print("Aqui está a predição do modelo:")
print(predicao)



# Configuração de logging
logging.basicConfig(level=logging.DEBUG)


# Informações da API para documentação
info = Info(title="PedraGPT", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definição dos tags para a documentação
home_tag = Tag(name="Home", description="Redireciona para a documentação da API")
ml_tag = Tag(name="Canoas", description="Pesquisa e informações sobre canoas")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')


## Consulta modelo de classificação para estimar a existência ou não de pedras nos rins:

#@app.post('/consultamodelo', tags=[ml_tag_tag], responses={"200": CanoeQueryResponse, "400": ErrorResponse})
@app.post('/consultamodelo', tags=[ml_tag])
def estima_existencia_pedras_rins(body):  #estima_existencia_pedras_rins(body: CanoeQueryRequest):
    return 1


## Execução

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

