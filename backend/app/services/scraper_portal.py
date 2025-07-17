import sys
import logging
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.chrome_driver_opcoes import criar_driver, fechar_driver, imagem_tela

logger = logging.getLogger("scraper")
logger.setLevel(logging.DEBUG)
if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class PortalTransparenciaScraper:
    def __init__(self):
        self.driver, self.user_data_dir = criar_driver()
        self.wait = WebDriverWait(self.driver, 15)

    def close(self):
        fechar_driver(self.driver, self.user_data_dir)

    def buscar_pessoa(self, termo_busca: str):
        resultado_final = {
            "termo_busca": termo_busca,
            "resultado": [],
            "mensagem_erro": None
        }

        try:
            logger.info(f"Iniciando busca por: {termo_busca}")
            self.driver.get("https://portaldatransparencia.gov.br/pessoa/visao-geral")
            imagem_tela(self.driver, "pag")

            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accept-all-btn"]'))).click()
            imagem_tela(self.driver, "pag")

            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="button-consulta-pessoa-fisica"]'))).click()
            imagem_tela(self.driver, "pag")

            input_busca = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="termo"]')))
            imagem_tela(self.driver, "pag")
            input_busca.clear()
            input_busca.send_keys(termo_busca)
            imagem_tela(self.driver, "pag")

            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-superior"]/section[1]/div/div/fieldset/div/button'))).click()
            imagem_tela(self.driver, "pag")
            
            checkbox = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accordion1"]/div[1]/button')))
            imagem_tela(self.driver, "pag")
            if not checkbox.is_selected():
                checkbox.click()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="box-busca-refinada"]/div[1]/div[2]/div'))).click()
            imagem_tela(self.driver, "pag")
            
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnConsultarPF"]')))
            imagem_tela(self.driver, "pag")
            
            resultado_beneficios = self.driver.find_elements(By.XPATH, '//*[@id="resultados"]')[:10]
            imagem_tela(self.driver, "pag")

            if not resultado_beneficios:
                logger.warning(f"Nenhum resultado encontrado para '{termo_busca}'")
                resultado_final["mensagem_erro"] = f"Nenhum resultado encontrado para '{termo_busca}'."
                return resultado_final

            logger.info(f"Encontrados {len(resultado_beneficios)} resultados")
            for idx, linha in enumerate(resultado_beneficios):
                linha.click()
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//h1[contains(text(),"Panorama da relação")]')))

                screenshot_b64 = self.driver.get_screenshot_as_base64()
                beneficios = self._coletar_beneficios()

                resultado_final["resultado"].append({
                    "indice": idx + 1,
                    "beneficios": beneficios,
                    "screenshot_base64": screenshot_b64
                })

                self.driver.back()
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody')))

            return resultado_final

        except TimeoutException:
            logger.error("Timeout: Portal demorou para responder.")
            resultado_final["mensagem_erro"] = "Tempo esgotado ao buscar dados no portal."
            return resultado_final
        except Exception as e:
            logger.exception("Erro inesperado durante a busca")
            resultado_final["mensagem_erro"] = f"Erro inesperado: {str(e)}"
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
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.detalhe-beneficio')))
                    info = self.driver.find_element(By.CSS_SELECTOR, 'div.detalhe-beneficio').text
                    beneficios.append(info)
                    self.driver.back()
                    self.wait.until(EC.presence_of_element_located((By.XPATH, '//h1[contains(text(),"Panorama da relação")]')))
                except NoSuchElementException:
                    beneficios.append(row.text)
        except Exception as e:
            logger.warning(f"Erro coletando benefícios: {e}")
        return beneficios