import os
import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
#from fastapi.params import Body
#from typing import Optional, List
import psycopg2
#from . import utils
#from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, get_db
from .routers import post, user, auth


DB_PASSWORD = os.getenv('DB_PASSOWRD')


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#test the data send to API

while True: 
    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password=DB_PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to my api"}



