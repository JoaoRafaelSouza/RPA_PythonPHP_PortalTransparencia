from db import Base, engine
from models.pessoa_model import Pessoa
from models.beneficio_model import Beneficio

print("Criando as tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso.")