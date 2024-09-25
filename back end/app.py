# app.py
import requests
import logging

from flask import jsonify, redirect
from pydantic import BaseModel
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag

import pickle #para desserializar o modelo


#Imports to Scikit Learn ==> iguais ao usado no modelo
from sklearn.preprocessing import StandardScaler #Padronização dos dados
from sklearn.preprocessing import MinMaxScaler #Normalização dos dados
from sklearn.model_selection import train_test_split #Divisão do dataset em conjuntos para treino e teste
from sklearn.model_selection import KFold #Para validação cruzada
from sklearn.model_selection import StratifiedKFold #Variante do Kfold, para manter o número de classes em cada fold
from sklearn.model_selection import cross_val_score #Para determinar a pontuação em rotinas de cross validation
from sklearn.model_selection import GridSearchCV #Para otimização de hiperparâmetros
from sklearn.metrics import accuracy_score #Pontuação pela métrica de acurácia
from sklearn.pipeline import Pipeline #Para pipelinas (normalização -> classificação, ou padronização -> classificação)
from sklearn.tree import DecisionTreeClassifier #Árvore de Classificação
from sklearn.neighbors import KNeighborsClassifier #KNN
from sklearn.naive_bayes import GaussianNB #Naive Bayes
from sklearn.svm import SVC #Support Vector Machine

from schemas_comm_back_front import *

from classes.model_loader import ModelLoader

# Carregando o modelo de ML exportado a partir do Notebook Colab
'''
endereco_do_modelo = "./modelo_ml/classifier skl version 1_5_2.pkl" 
# coloco no nome do arquivo a versão do Scikit Learning usada para gerar o modelo
# a versão usada para gerar o modelo deve ser a mesma versão importada aqui no back end
# assim garantimos a compatibilidade de modelos

pickle_in = open(endereco_do_modelo, 'rb')
modelo = pickle.load(pickle_in)
pickle_in.close()

# Carregando o scaler
endereco_do_scaler = "./modelo_ml/scaler skl version 1_5_2.pkl" 
pickle_in = open(endereco_do_scaler, 'rb')
scaler = pickle.load(pickle_in)
pickle_in.close()
'''

# Carregar as configurações do modelo e scaler
model_loader = ModelLoader()

# Carregar o modelo e o scaler
modelo = model_loader.get_model()
scaler = model_loader.get_scaler()


# Testando
teste = [1.021, 4.9, 725, 14, 443, 2.45]
input_teste_normalized = scaler.transform([teste]) # Normalizar os dados com o normalizador carregado
predicao = modelo.predict(input_teste_normalized)
print(f"Dados de entrada: {teste}")
print(f"Dados padronizados: {input_teste_normalized}")
print(f"Resultado da predição com dados de teste: {predicao[0]}")
print("Se não teve falha aqui, então o modelo deve ter sido importado corretamente")



# Configuração de logging
logging.basicConfig(level=logging.DEBUG)


# Informações da API para documentação
info = Info(title="PedraGPT", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definição dos tags para a documentação
home_tag = Tag(name="Home", description="Redireciona para a documentação da API")
ml_tag = Tag(name="Modelo ML", description="Retorna o resultado da predição do modelo a partir de um conjunto de dados referentes a uma instância")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')


## Consulta modelo de classificação para estimar a existência ou não de pedras nos rins:

@app.post('/consultamodelo', tags=[ml_tag], responses={"200": SchemaPrediction, "400": SchemaMensagemErro})
def estima_existencia_pedras_rins(body: SchemaExam):  #estima_existencia_pedras_rins
    print(body)
    input = []
    input.append(body.gravidade)
    input.append(body.pH)
    input.append(body.osmolaridade)
    input.append(body.condutividade)
    input.append(body.ureia)
    input.append(body.calcio)
    print(f"Dados de entrada: {input}")
    
    standardized_input = scaler.transform([input]) # Normalizar os dados de entrada com o padronizador carregado
    print(f"Dados de entrada padronizados: {standardized_input}")
    
    predicao = modelo.predict(standardized_input) ##Aqui a mágica acontece!
    print(f"Resultado da predição com dados de entrada padronizados: {predicao}")
      
     
    #Converter o resultado numérico em texto
    if predicao[0] == 1:
        answer = "Sim, provavelmente tem pedra nos rins"
    else:
        answer = "Não, provavelmente não tem pedra nos rins"
    
     
    #comunicar a resposta
    print(f"Resultado: {answer}")
    print("Predição entregue sem falhas") 
    return {"resultado": answer}




## Execução

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

