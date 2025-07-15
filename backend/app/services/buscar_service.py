from models.consulta_model import ConsultaRequest

async def buscar_dados(body: ConsultaRequest):
    if body.cpf:
        return {"resultado": f"Consulta CPF {body.cpf}"}
    elif body.nis:
        return {"resultado": f"Consulta NIS {body.nis}"}
    elif body.nome:
        return {"resultado": f"Consulta Nome {body.nome}"}
    return {"erro": "Nenhum dado informado"}
