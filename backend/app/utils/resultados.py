import json
import os
from datetime import datetime

def salvar_em_arquivo_json(dados, nome_arquivo="resultado_busca.json", pasta="logs"):
    # Cria a pasta se não existir
    os.makedirs(pasta, exist_ok=True)

    # Nome do arquivo com data/hora para evitar sobrescrita
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_arquivo = os.path.join(pasta, f"{timestamp}_{nome_arquivo}")

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    return caminho_arquivo