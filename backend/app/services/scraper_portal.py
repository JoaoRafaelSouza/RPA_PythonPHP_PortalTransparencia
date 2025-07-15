import base64
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PortalTransparenciaScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--remote-debugging-port=9222")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)

    def close(self):
        self.driver.quit()

    def buscar_pessoa(self, termo_busca: str):
        resultado_final = {
            "termo_busca": termo_busca,
            "resultado": [],
            "mensagem_erro": None
        }

        try:
            # Passo 1 e 2 - Acessar portal e clicar em "Acessar busca" para Pessoa Física
            self.driver.get("https://portaldatransparencia.gov.br/pessoa/visao-geral")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Acessar busca")]'))).click()

            # Passo 3 - Preencher campo busca
            input_busca = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'input[placeholder*="Nome, Nis ou CPF"]')))
            input_busca.clear()
            input_busca.send_keys(termo_busca)

            # Passo 4 - Expandir "REFINE A BUSCA" e marcar "BENEFICIÁRIO DE PROGRAMA SOCIAL"
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(),"REFINE A BUSCA")]'))).click()
            checkbox = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//label[contains(text(),"BENEFICIÁRIO DE PROGRAMA SOCIAL")]/preceding-sibling::input[@type="checkbox"]')))
            if not checkbox.is_selected():
                checkbox.click()

            # Passo 5 - Clicar em "Consultar"
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(),"Consultar")]'))).click()

            # Passo 6 - Coletar resultados, até 10 primeiros
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody')))
            linhas = self.driver.find_elements(By.CSS_SELECTOR, 'tbody tr')[:10]

            if len(linhas) == 0:
                resultado_final["mensagem_erro"] = f'Foram encontrados 0 resultados para o termo "{termo_busca}".'
                return resultado_final

            for idx, linha in enumerate(linhas):
                # Clicar na linha para abrir detalhes
                linha.click()
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//h1[contains(text(),"Panorama da relação")]')))

                # Capturar screenshot como base64
                screenshot_b64 = self.driver.get_screenshot_as_base64()

                # Coletar benefícios
                beneficios = self._coletar_beneficios()

                resultado_final["resultado"].append({
                    "indice": idx + 1,
                    "beneficios": beneficios,
                    "screenshot_base64": screenshot_b64
                })

                # Voltar para a lista
                self.driver.back()
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody')))

            return resultado_final

        except TimeoutException:
            resultado_final["mensagem_erro"] = "Não foi possível retornar os dados no tempo de resposta solicitado."
            return resultado_final
        except Exception as e:
            resultado_final["mensagem_erro"] = f"Erro inesperado: {str(e)}"
            logger.error(f"Erro na busca: {e}", exc_info=True)
            return resultado_final
        finally:
            self.close()

    def _coletar_beneficios(self):
        beneficios = []
        try:
            rows = self.driver.find_elements(By.CSS_SELECTOR, 'div.lista-beneficios > div.beneficio')
            for row in rows:
                try:
                    detalhar_btn = row.find_element(By.XPATH, './/button[contains(text(),"Detalhar")]')
                    detalhar_btn.click()
                    self.wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'div.detalhe-beneficio')))
                    info = self.driver.find_element(By.CSS_SELECTOR, 'div.detalhe-beneficio').text
                    beneficios.append(info)
                    self.driver.back()
                    self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//h1[contains(text(),"Panorama da relação")]')))
                except NoSuchElementException:
                    # Se não tiver detalhar, pegar o texto direto
                    info = row.text
                    beneficios.append(info)
        except Exception as e:
            logger.warning(f"Erro coletando benefícios: {e}")
        return beneficios