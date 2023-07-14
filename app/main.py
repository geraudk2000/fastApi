import os
import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg2
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db


DB_PASSWORD = os.getenv('DB_PASSOWRD')


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#test the data send to API
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None 

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
    


my_posts = [{"title": "title of posts 1", "content": "content of post 1", "id" : 1},
            {"title": "favorite foods", "content": "I like pizza", "id" : 2}]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
    return None

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

@app.get("/")
def root():
    return {"message": "Welcome to my api"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(posts: Post, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (posts.title, posts.content, posts.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(title=posts.title, content=posts.content, published=posts.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
# title str, content str,


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first() 

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} was not found")
        
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()
    #find the index in the array that has required ID
    index = find_index_post(id)
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published, str(id)))
    
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"post with {id} was not found")
    
    return {"data": updated_post}