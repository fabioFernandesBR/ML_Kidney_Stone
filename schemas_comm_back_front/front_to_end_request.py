from pydantic import BaseModel


class SchemaExam(BaseModel):
    """ Define como deve ser a estrutura que representa a comunicação entre o Front e o Back end
        para informar os dados sobre o exame de urina do paciente. 
    """
    gravidade: float
    osmolaridade: float
    condutividade: float
    pH: float
    ureia: float
    calcio: float

