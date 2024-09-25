from pydantic import BaseModel


class SchemaPrediction(BaseModel):
    """ Define como deve ser a estrutura que representa a comunicação entre o BAck e o Front end
        para informar os resultado da previsão do modelo. 
    """
    resultado: str