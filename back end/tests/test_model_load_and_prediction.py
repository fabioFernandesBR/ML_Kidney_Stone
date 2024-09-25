import pytest
import numpy as np
from classes import ModelLoader
import csv
import os
from app import app

@pytest.fixture
def model_loader():
    return ModelLoader()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_model_loader_loads_model_and_scaler(model_loader):
    # Testar se o modelo é carregado corretamente
    modelo = model_loader.get_model()
    assert modelo is not None, "O modelo não foi carregado corretamente."
    assert hasattr(modelo, 'predict'), "O modelo carregado não possui o método 'predict'."

    # Testar se o scaler é carregado corretamente
    scaler = model_loader.get_scaler()
    assert scaler is not None, "O scaler não foi carregado corretamente."
    assert hasattr(scaler, 'transform'), "O scaler carregado não possui o método 'transform'."

def test_model_prediction(model_loader):
    # Testar se o modelo retorna outputs esperados: número igual a 0 ou 1.
    
    # Carregar o modelo e o scaler
    modelo = model_loader.get_model()
    scaler = model_loader.get_scaler()

    # Dados de teste
    input_data = np.array([[5.1, 3.5, 1.4, 0.2, 4, 6]])  #números quaisquer

    # Escalar e fazer a previsão
    scaled_data = scaler.transform(input_data)
    prediction = modelo.predict(scaled_data)

    # Verificar se a previsão é válida
    assert isinstance(prediction[0], (int, float)), "A previsão deve ser um número."
    assert prediction[0] == 0 or prediction[0] == 1, "A previsão deve ser 0 ou 1."

def test_model_with_csv_input(model_loader):
    # Verificar se as previsões a partir de um conjunto de dados batem com os resultados esperados
    
    # Carregar o modelo e o scaler
    modelo = model_loader.get_model()
    scaler = model_loader.get_scaler()

    # Caminho do arquivo CSV
    csv_file_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')

    # Abrir o arquivo CSV e processar os dados
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Pular o cabeçalho

        for row in reader:
            # Pegar os dados de entrada (primeiras 6 colunas) e a saída esperada (última coluna)
            input_data = np.array([row[:6]], dtype=float)  # Dados de entrada
            expected_output = float(row[6])  # Target

            # Escalar os dados de entrada
            scaled_data = scaler.transform(input_data)

            # Fazer a previsão com o modelo
            prediction = modelo.predict(scaled_data)

            # Verificar se a previsão é igual ao valor esperado
            assert prediction[0] == expected_output, f"Esperado {expected_output}, mas obteve {prediction[0]}"

def test_predict_valid_input(client):
    # Enviar dados válidos para a API
    valid_data = {
        "gravidade": 1.021,
        "pH": 4.91,
        "osmolaridade": 725,
        "condutividade": 14,
        "ureia": 443,
        "calcio": 2.45
    }
    
    response = client.post('/consultamodelo', json=valid_data)

    # Verificar se o código de status é 200
    assert response.status_code == 200, f"Erro: {response.data}"

def test_predict_invalid_input(client):
    # Enviar dados inválidos (faltando campos, por exemplo)
    invalid_data = {
        "gravidade": 1.021,
        "pH": 4.91
        # O resto dos dados está faltando
    }
    
    response = client.post('/consultamodelo', json=invalid_data)

    # Espero o código 422, UNPROCESSABLE ENTITY, que é o que acontece quando o schema definido no Pydantic não é obedecido.
    assert response.status_code == 422, f"Erro esperado 422, mas obteve {response.status_code}"
