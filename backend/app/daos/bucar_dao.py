from db import SessionLocal
from models.pessoa_model import Pessoa
from models.beneficio_model import Beneficio
import logging

logger = logging.getLogger("persistencia")

def salvar_resultados_no_banco(resultado: dict, cpf=None, nis=None, nome=None):
    db = SessionLocal()
    try:
        pessoa = Pessoa(cpf=cpf, nis=nis, nome=nome)
        db.add(pessoa)
        db.flush()  # garante que o ID da pessoa seja gerado

        for item in resultado.get("resultado", []):
            beneficio = Beneficio(
                beneficio="\n".join(item.get("beneficios", [])),
                imagem_base64=item.get("screenshot_base64"),
                pessoa_id=pessoa.id
            )
            db.add(beneficio)

        db.commit()
        print("Pessoa e benefícios salvos com sucesso.")
    except Exception as e:
        db.rollback()
        print("Erro ao salvar no banco:", str(e))
    finally:
        db.close()