import tempfile
import shutil
import logging
import sys
import time
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException

logger = logging.getLogger("chrome_driver")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s"))
    logger.addHandler(handler)

def criar_driver(tentativas=3):
    for tentativa in range(1, tentativas + 1):
        unique_id = f"{int(time.time())}_{uuid.uuid4().hex[:8]}"
        user_data_dir = tempfile.mkdtemp(prefix=f"chrome_profile_{unique_id}_")

        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

            logger.info(f"[Tentativa {tentativa}] Iniciando Chrome com: {user_data_dir}")
            driver = webdriver.Chrome(options=chrome_options)
            return driver, user_data_dir

        except SessionNotCreatedException as e:
            logger.warning(f"[Tentativa {tentativa}] Erro de sessão: {e}")
            shutil.rmtree(user_data_dir, ignore_errors=True)
            time.sleep(1)

        except Exception as e:
            logger.error(f"[Tentativa {tentativa}] Erro inesperado: {e}")
            shutil.rmtree(user_data_dir, ignore_errors=True)
            raise

    raise RuntimeError("Falha ao criar WebDriver após múltiplas tentativas")

def fechar_driver(driver, user_data_dir):
    logger.info("Encerrando WebDriver e limpando perfil temporário")
    try:
        driver.quit()
    except Exception as e:
        logger.warning(f"Erro ao encerrar driver: {e}")
    try:
        shutil.rmtree(user_data_dir, ignore_errors=True)
    except Exception as e:
        logger.warning(f"Erro ao remover perfil temporário: {e}")