from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randint


app = FastAPI()

#test the data send to API
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None 


my_posts = [{"title": "title of posts 1", "content": "content of post 1", "id" : 1},
            {"title": "favorite foods", "content": "I like pizza", "id" : 2}]

@app.get("/")
def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(posts: Post):
    post_dict = posts.dict()
    post_dict['id'] = randint(0, 10000000)
    my_posts.append(post_dict)
    return {"data": my_posts}
# title str, content str,