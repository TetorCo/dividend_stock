from sqlalchemy import create_engine, Column, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import date

import os
import dotenv

dotenv.load_dotenv()

## PostgreSQL Info
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))
DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"
table = "stock_info"

## SQLAlchemy Engine Setting
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

## DB Model Define
base = declarative_base()

class Data(base):
    __tablename__ = table

    code = Column(String(length=10), primary_key=True)
    cost = Column(Float)
    dividend_rate = Column(Float)
    ex_date = Column(Date)
    pay_date = Column(Date)


def mongodb_data_to_postgresql(stock_list):
    """
    index_info
    0 : stock_code
    1 : dividend_rate
    2 : ex_date
    3 : pay_date
    4 : cost
    """
    for stock_info in stock_list:
        ex_date = date(stock_info[2]['year'], stock_info[2]['month'], stock_info[2]['day'])
        pay_date = date(stock_info[3]['year'], stock_info[3]['month'], stock_info[3]['day'])

        load_data = Data(code = stock_info[0],
                        cost = stock_info[4],
                        dividend_rate = stock_info[1],
                        ex_date = ex_date,
                        pay_date = pay_date)
        
        session.add(load_data)

    session.commit()
    session.close()


if __name__ == "__main__":

    test = [["UTG", 0.19, {"year": 2024, "month": 1, "day": 17}, {"year": 2023, "month": 12, "day": 28}, 26.62]]
    # print(test[2])
    mongodb_data_to_postgresql(test)