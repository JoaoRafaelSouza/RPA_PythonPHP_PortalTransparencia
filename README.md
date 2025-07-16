# RPA_PythonPHP_PortalTransparencia
Criado o docker para usar PHP com Python, e com banco de dados Mysql, faz uma busca no site Portal da Transparencia "https://portaldatransparencia.gov.br/pessoa/visao-geral", fazendo uma pesquisa através de Nome ou CPF ou Nis, a resposta é entregue em Json e salva os dados no MySql.

# 🕵️‍♂️ RPA Portal da Transparência - Simples

Automação (RPA) com Python/FastAPI para extração de dados do Portal da Transparência do Governo Federal. Realiza busca por CPF, NIS ou Nome, armazena os dados em MySQL e permite acesso via API RESTful. Projeto pronto para produção com Docker, CI/CD e layout escalável.

---

## 🚀 Funcionalidades

- 🔎 Web Scraping com Selenium e Tesseract OCR
- 🧾 Extração de dados de benefícios (Bolsa Família, Auxílio Brasil, etc.)
- 💾 Armazenamento em banco MySQL
- 📦 API RESTful com FastAPI
- 🔐 Variáveis de ambiente seguras
- 🐳 Docker e Docker Compose
- 🔁 CI/CD via GitHub Actions
- 📊 Exportação para visualização futura no Power BI

---

## 📁 Estrutura do Projeto
Está na pasta docs, e o arquivo é Estrutura.txt


---

## 🛠️ Tecnologias

- Python 3.9+
- FastAPI
- SQLAlchemy + Alembic
- MySQL 8+
- Selenium + ChromeDriver
- pytesseract (OCR)
- Docker
- GitHub Actions (CI/CD)

---

## ⚙️ Como Rodar o Projeto (modo Docker)

### Pré-requisitos

- Docker
- Docker Compose

### Passos

1. Clone o repositório

```bash
git clone https://github.com/JoaoRafaelSouza/RPA_PythonPHP_PortalTransparencia.git
cd RPA_PythonPHP_PortalTransparencia

infra/.env
env
Copiar
Editar
MYSQL_ROOT_PASSWORD=123
MYSQL_DATABASE=rpa
MYSQL_USER=admin
MYSQL_PASSWORD=123
MYSQL_HOST=mysql
infra/.env.local
env
Copiar
Editar
MYSQL_ROOT_PASSWORD=123
MYSQL_DATABASE=rpa
MYSQL_USER=admin
MYSQL_PASSWORD=123
MYSQL_HOST=localhost
Suba os containers:

bash
Copiar
Editar
docker-compose up --build
Acesse:

📬 API: http://localhost:8000

📚 Swagger: http://localhost:8000/docs

🔒 Redoc: http://localhost:8000/redoc

🧪 Testes
Execute os testes com:

bash
Copiar
Editar
cd backend
pytest
🧩 Endpoints da API
Método	Endpoint	Descrição
GET	/	Testa se a API está online
POST	/api/buscar	Faz a busca por CPF/NIS/Nome

📦 Migrations (Alembic)
Criar nova migration
bash
Copiar
Editar
alembic revision --autogenerate -m "descrição"
Aplicar migration
bash
Copiar
Editar
alembic upgrade head
🔐 Segurança e Produção
As senhas do banco e tokens estão isoladas em .env

O Chrome roda em modo headless com sandbox desativado

O projeto é preparado para deploy em nuvem com NGINX reverso

📄 Documentação extra
Veja a pasta docs/ para:

Comandos úteis em Docker

Solução de erros

Estrutura de pastas explicada

Logs e limpeza de volumes

🧠 Autor
João Rafael Quintiliano de Souza
🔗 GitHub
🌐 Site

📜 Licença
MIT © 2025 João Rafael Quintiliano