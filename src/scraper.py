import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import smtplib
from email.mime.text import MIMEText

load_dotenv()

chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")

chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = os.getenv("URL_PRODUTO")

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Preco(Base):
    __tablename__ = "precos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False)
    preco = Column(DECIMAL(10, 2), nullable=False)
    preco_anterior = Column(DECIMAL(10, 2))  # Novo campo adicionado
    data_registro = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


Base.metadata.create_all(bind=engine)


def enviar_email(preco_anterior, preco_atual):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")

    msg = MIMEText(
        f"O preço do produto mudou de R${preco_anterior} para R${preco_atual}."
    )
    msg["Subject"] = "Alerta de Mudança de Preço"
    msg["From"] = email_from
    msg["To"] = email_to

    try:
        print(f"Resolvendo {smtp_server}:{smtp_port}")
        socket.gethostbyname(smtp_server)
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(email_from, [email_to], msg.as_string())
        server.quit()
        print("E-mail de alerta enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def extract_and_save_price(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "andes-money-amount"))
        )
        price_element = driver.find_element(By.CLASS_NAME, "andes-money-amount")

        if price_element:
            price_text = price_element.text.strip()
            print(f"Preço encontrado: {price_text}")

            if price_text:
                # Limpar e formatar o preço
                cleaned_price = (
                    price_text.replace("R$", "")
                    .replace("\n", "")
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                )
                try:
                    cleaned_price_decimal = float(cleaned_price)
                except ValueError:
                    print(f"Erro ao converter preço: {cleaned_price}")
                    return None

                # Salvar no banco de dados
                db = SessionLocal()
                ultimo_preco = (
                    db.query(Preco)
                    .filter(Preco.url == url)
                    .order_by(Preco.data_registro.desc())
                    .first()
                )

                if ultimo_preco:
                    if ultimo_preco.preco != cleaned_price_decimal:
                        preco_anterior = ultimo_preco.preco
                        novo_preco = Preco(
                            url=url,
                            preco=cleaned_price_decimal,
                            preco_anterior=preco_anterior,
                        )
                        db.add(novo_preco)
                        db.commit()
                        enviar_email(preco_anterior, cleaned_price_decimal)
                    else:
                        print("O preço não mudou.")
                else:
                    novo_preco = Preco(url=url, preco=cleaned_price_decimal)
                    db.add(novo_preco)
                    db.commit()

                db.close()
                return cleaned_price_decimal
            else:
                print("Texto do preço está vazio.")
                return None
        else:
            print("Elemento de preço não encontrado.")
            return None
    except Exception as e:
        print(f"Erro ao extrair e salvar preço: {e}")
        return None
    finally:
        driver.quit()


if __name__ == "__main__":
    preco_atual = extract_and_save_price(url)
    if preco_atual:
        print(f"Preço atual do produto: {preco_atual}")
