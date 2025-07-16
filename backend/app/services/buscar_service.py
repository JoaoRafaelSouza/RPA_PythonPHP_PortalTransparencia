from models.consulta_model import ConsultaRequest
from .scraper_portal import PortalTransparenciaScraper
from utils.resultados import salvar_em_arquivo_json
import logging
import sys

logger = logging.getLogger("buscar_service")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

async def buscar_dados(body: ConsultaRequest):
    termo_busca = body.cpf or body.nis or body.nome
    if not termo_busca:
        logger.warning("Nenhum termo de busca fornecido.")
        return {"erro": "Nenhum dado informado. Informe CPF, NIS ou Nome."}

    try:
        logger.info(f"Iniciando busca para: {termo_busca}")
        scraper = PortalTransparenciaScraper()
        resultado = scraper.buscar_pessoa(termo_busca)
        logger.info("Busca concluída com sucesso.")

        caminho_arquivo = salvar_em_arquivo_json(resultado)
        logger.info(f"Resultado salvo em: {caminho_arquivo}")

        return resultado
    except Exception as e:
        logger.exception("Erro durante o processo de busca.")
        return {"erro": "Erro interno ao executar a busca. Verifique os logs."}