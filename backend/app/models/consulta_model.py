from pydantic import BaseModel
from typing import Optional

class ConsultaRequest(BaseModel):
    cpf: Optional[str] = None
    nis: Optional[str] = None
    nome: Optional[str] = None

def buscar_dados(dados):
    # exemplo fictício
    cpf = dados.get("cpf")
    if not cpf:
        raise ValueError("CPF é obrigatório")
    return {"cpf": cpf}