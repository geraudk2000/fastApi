from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor


DB_PASSWORD = os.getenv('DB_PASSOWRD')
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


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(posts: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   (posts.title, posts.content, posts.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}
# title str, content str,

@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[len(my_posts) - 1]
    return {"detail": latest_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} was not found")
        
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #find the index in the array that has required ID
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"post with {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}