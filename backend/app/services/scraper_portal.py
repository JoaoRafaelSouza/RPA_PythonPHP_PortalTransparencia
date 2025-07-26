import sys
import logging
import time
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
            # Aqui inicia 
            logger.info(f"Iniciando busca por: {termo_busca}")
            self.driver.get("https://portaldatransparencia.gov.br/pessoa/visao-geral")
            imagem_tela(self.driver, "pag")

            # Faz o primeiro acesso ao portal
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="button-consulta-pessoa-fisica"]'))).click()
            time.sleep(10)
            imagem_tela(self.driver, "pag")
            
            # Faz o clique, aceita os cookies
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accept-all-btn"]'))).click()
            time.sleep(2)
            imagem_tela(self.driver, "pag")

            # Aqui ele habilita o cursor para fazer input como nome, cpf ou nis
            input_busca = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="termo"]')))
            time.sleep(2)
            imagem_tela(self.driver, "pag")
            input_busca.clear()
            
            #Aqui ele coloca o valor do input
            input_busca.send_keys(termo_busca)
            time.sleep(2)
            imagem_tela(self.driver, "pag")

            # Aqui ele abre o checkbox da tela
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-superior"]/section[1]/div/div/fieldset/div/button'))).click()
            time.sleep(2)
            imagem_tela(self.driver, "pag")
            
            # Aqui ele faz o clique para abrir o tipo de pesquisa.
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accordion1"]/div[1]/button'))).click()
            time.sleep(2)
            imagem_tela(self.driver, "pag")
            
            # Aqui seleciona a opção Beneficiário de Programa Social
            checkbox = self.driver.find_element(By.XPATH, '//*[@id="box-busca-refinada"]/div[1]/div[2]/div/label')
            if not checkbox.is_selected():
                checkbox.click()
            time.sleep(2)
            imagem_tela(self.driver, "pag")

            # Aqui ele confirma a pesquisa
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnConsultarPF"]'))).click()
            time.sleep(5)
            imagem_tela(self.driver, "pag")
            
            qtde_resultado = self.driver.find_element(By.ID, 'countResultados')
            time.sleep(10)
            imagem_tela(self.driver, "pag")
            
            if(int(qtde_resultado.text) == 0):
                logger.warning(f"Nenhum resultado encontrado para '{termo_busca}'")
                resultado_final["mensagem_erro"] = f"Nenhum resultado encontrado para '{termo_busca}'."
                return resultado_final

            # Aqui ele faz o clique no nome da pessoa
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.link-busca-nome'))).click()
            time.sleep(15)
            imagem_tela(self.driver, "pag")
            
            # Aqui ele clica novamente no aceitar cookies na tela Pessoa Física
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accept-all-btn"]'))).click()
            imagem_tela(self.driver, "pag")
            
            icone = self.driver.find_element(By.CSS_SELECTOR, 'div.item i.fas')
            time.sleep(2)
            classe = icone.get_attribute("class")
            if "fa-angle-down" in classe:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accordion1"]/div[1]/button'))).click()
                time.sleep(2)
                imagem_tela(self.driver, "pag")
            
            for idx in range(10):
                todos_botoes = self.driver.find_elements(By.CSS_SELECTOR, '.br-button.secondary.mt-3')
                resultado_beneficios = [el for el in todos_botoes if 'block' not in el.get_attribute('class')]
                
                if idx >= len(resultado_beneficios):
                    break
                
                linha = resultado_beneficios[idx]
                linha.click()
                time.sleep(10)
                imagem_tela(self.driver, "pag")
                
                screenshot_b64 = self.driver.get_screenshot_as_base64()
                beneficios = self._coletar_beneficios()
                imagem_tela(self.driver, "pag")
                
                resultado_final["resultado"].append({
                    "indice": idx + 1,
                    "beneficios": beneficios,
                    "screenshot_base64": screenshot_b64
                })

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
        try:
            # Pega o título do beneficiário
            titulo = self.driver.find_element(By.CSS_SELECTOR, '.py-0.px-0.mx-0.mt-0.mb-2.mb-md-0.pb-0.text-left').text.strip()
            time.sleep(2)

            icone = self.driver.find_element(By.CSS_SELECTOR, 'div.item i.fas')
            time.sleep(2)
            classe = icone.get_attribute("class")
            # Verifica se a classe está igual e expande os detalhes do auxílio
            if "fa-angle-up" in classe:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accordion1"]/div[1]/button'))).click()
                time.sleep(2)
                imagem_tela(self.driver, "pag")
            
            # Aqui ele clica novamente no aceitar cookies na tela Pessoa Física
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accept-all-btn"]'))).click()
            imagem_tela(self.driver, "pag")
            
            btnPag = self.driver.find_element(By.ID, 'btnPaginacaoCompleta')
            time.sleep(2)
            classe = btnPag.get_attribute("class")
            if "br-button" in classe:
                self.wait.until(EC.element_to_be_clickable((By.ID, 'btnPaginacaoCompleta'))).click()
                time.sleep(2)
                imagem_tela(self.driver, "pag")
                self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tabelaDetalheValoresSacados_length"]/label/select/option[3]'))).click()
                time.sleep(2)
                imagem_tela(self.driver, "pag")
                
            tabela = self.driver.find_element(By.XPATH,'//*[@id="tabelaDetalheValoresSacados"]')
            time.sleep(2)
            
            # Coleta os títulos das colunas
            cabecalhos = [th.text.strip() for th in tabela.find_elements(By.CSS_SELECTOR, 'thead tr th')]
            time.sleep(2)
            
            # Aqui pegamos todas as linhas do tbody
            linhas = tabela.find_elements(By.CSS_SELECTOR, 'tbody tr')
            time.sleep(2)
            
            # Aqui temos um arrray que servirá de lista no final
            beneficio = []

            for linha in linhas:
                try:
                    colunas = linha.find_elements(By.TAG_NAME, 'td')
                    time.sleep(2)
                    dados = [td.text.strip() for td in colunas]
                    time.sleep(2)

                    if len(dados) == len(cabecalhos):
                        beneficio.append(dict(zip(cabecalhos, dados)))
                        time.sleep(2)
                    else:
                        logger.warning(f"[{titulo}] Qtd de colunas diferente dos títulos: {dados}")
                except Exception as e:
                    logger.warning(f"[{titulo}] Erro processando linha: {e}")

            return {titulo: beneficio}

        except Exception as e:
            logger.warning(f"Erro geral coletando benefícios: {e}")
            return {}