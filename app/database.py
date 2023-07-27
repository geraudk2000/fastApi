from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import psycopg2
import os
import time


DB_PASSWORD = os.getenv('DB_PASSOWRD')
DB_URL_DEV = os.getenv('DB_URL_DEV')

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Kcgeraud1986!@localhost/fastapi"

engine = create_engine(DB_URL_DEV)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True: 
#     try: 
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#                                 password=DB_PASSWORD, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print("connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
