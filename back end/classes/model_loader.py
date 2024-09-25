import json
import os
import pickle

class ModelLoader:
    def __init__(self):
        # Define o caminho absoluto para o arquivo de configuração
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Um nível acima da pasta 'classes'
        self.config_file = os.path.join(base_dir, 'model_ml', 'config.json')  # Caminho correto para o config.json
        self.model = None
        self.scaler = None
        self.load_config()

    def load_config(self):
        # Verifica se o arquivo de configuração existe
        if not os.path.isfile(self.config_file):
            raise FileNotFoundError(f"Erro: O arquivo de configuração não foi encontrado em {self.config_file}")

        with open(self.config_file, 'r') as f:
            config = json.load(f)

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Um nível acima da pasta 'classes'
        model_name = config.get('modelo')
        model_path = os.path.join(base_dir, 'model_ml', model_name)
        print(f"importando {model_path}")
        scaler_name = config.get('scaler')
        scaler_path = os.path.join(base_dir, 'model_ml', scaler_name)
        print(f"importando {scaler_path}")

        self.load_model(model_path)
        self.load_scaler(scaler_path)

    def load_model(self, model_path):
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)

    def load_scaler(self, scaler_path):
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)

    def get_model(self):
        """Retorna o modelo carregado."""
        return self.model

    def get_scaler(self):
        """Retorna o scaler carregado."""
        return self.scaler
