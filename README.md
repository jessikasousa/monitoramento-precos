# Monitoramento de Preços com Selenium e Puppeteer

Este projeto tem como objetivo monitorar e alertar sobre mudanças de preços de um produto em um site de e-commerce. A aplicação utiliza Selenium e Puppeteer para navegar e extrair preços, e envia alertas por e-mail quando há mudanças significativas. Os dados históricos são armazenados em um banco de dados MySQL para análise futura.

## Tecnologias Utilizadas
- Python
- Selenium
- Node.js
- Puppeteer
- MySQL
- SQLAlchemy
- Dotenv

## Configuração do Ambiente

### 1. Instalar Dependências
Instale as dependências necessárias para Node.js:
```sh
npm install
```

Instale as dependências necessárias para Python:
```
pip install selenium sqlalchemy python-dotenv pymysql
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:
```
# Configurações do Selenium
CHROME_DRIVER_PATH=/path/to/chromedriver

# URL do produto a ser monitorado
URL_PRODUTO=

# Configurações do MySQL
SQLALCHEMY_DATABASE_URL=mysql+pymysql://username:password@localhost:3306/bd

# Configurações de e-mail
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=example@hotmail.com
SMTP_PASSWORD=suasenha
EMAIL_FROM=example@hotmail.com
EMAIL_TO=example@hotmail.com
```

### 3. Criar Banco de Dados
Crie um banco de dados MySQL e configure a URL de conexão no arquivo .env.

### 4. Executar o Script
Para executar o script Python e iniciar o monitoramento, utilize o comando:
```
python scraper.py
```

Para rodar o script Node.js e chamar o script Python, utilize o comando:
```
node index.js
```

### 5. Testar Alteração de Preços
Para testar a alteração manual de preços no banco de dados, execute:
```
python test_price_change.py
```

### Licença
Este projeto está licenciado sob a MIT License.