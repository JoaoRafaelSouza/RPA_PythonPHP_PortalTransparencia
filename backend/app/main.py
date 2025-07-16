from fastapi import FastAPI
import uvicorn
from controllers import buscar_controller
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, engine
from models import beneficio_model, pessoa_model
from dotenv import load_dotenv
from pathlib import Path
import logging
import os

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1].parent / 'infra' / '.env.local')

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT', '3306')}/{os.getenv('MYSQL_DATABASE')}"
)

engine = create_engine(DATABASE_URL)

logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("startup")

logger.info("Verificando/criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
logger.info("Verificação finalizada.")

app = FastAPI(title="RPA Portal da Transparência", description="API para scraping e extração de benefícios sociais.", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(buscar_controller.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API funcionando!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)