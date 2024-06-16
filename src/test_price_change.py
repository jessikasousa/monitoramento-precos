from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from scraper import Preco

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def change_product_price(new_price):
    db = SessionLocal()
    produto = db.query(Preco).order_by(Preco.data_registro.desc()).first()
    if produto:
        produto.preco = new_price
        db.commit()
        print(f"Preço do produto alterado para: {new_price}")
    db.close()


if __name__ == "__main__":
    new_price = 1500.00
    change_product_price(new_price)
    print(f"Preço de teste atualizado para: {new_price}")
