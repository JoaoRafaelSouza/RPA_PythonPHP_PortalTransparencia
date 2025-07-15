from models.consulta_model import ConsultaRequest
from fastapi import APIRouter
from services.buscar_service import buscar_dados

router = APIRouter()

@router.post("/buscar")
async def buscar_api(body: ConsultaRequest):
    resultado = await buscar_dados(body)
    return resultado