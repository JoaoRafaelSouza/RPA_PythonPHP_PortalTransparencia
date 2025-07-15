from pydantic import BaseModel
from typing import Optional

class ConsultaRequest(BaseModel):
    cpf: Optional[str] = None
    nis: Optional[str] = None
    nome: Optional[str] = None