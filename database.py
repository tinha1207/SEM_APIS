from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse
import os
from dotenv import load_dotenv
import mysql.connector


load_dotenv()
url = urllib.parse.quote_plus(os.environ["PASS"])

SQLALCHEMY_DATABASE_URL = f'mysql://{os.environ["USER"]}:{url}@{os.environ["HOST"]}:{os.environ["PORT"]}/{os.environ["DATABASE"]}'
SQLALCHEMY_DATABASE_URL_SEM = "mysql://tha:PaRc159187Et@127.0.0.1:3306"


engine_UDS = create_engine(SQLALCHEMY_DATABASE_URL)
engine_SEM = create_engine(SQLALCHEMY_DATABASE_URL_SEM)

SessionLocal_UDS = sessionmaker(autocommit=False, autoflush=False, bind=engine_UDS)
SessionLocal_SEM = sessionmaker(autocommit=False, autoflush=False, bind=engine_SEM)

Base = declarative_base()


def get_db_uds():
    try:
        db = SessionLocal_UDS()
        yield db
    finally:
        db.close()

def get_db_uds():
    try:
        db = SessionLocal_UDS()
        yield db
    finally:
        db.close()

def get_db_sem():
    try:
        db = SessionLocal_SEM()
        yield db
    finally:
        db.close()

def connect_ods():
    success_str = "Connection successful."
    conn = mysql.connector.connect(
        user=os.environ["USER"],
        password=os.environ["PASS"],
        host=os.environ["HOST"],
        database=os.environ["DATABASE"],
    )
    print(success_str)
    return conn


# Dependency
