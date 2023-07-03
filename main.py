from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
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

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
    return None

@app.get("/")
def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(posts: Post):
    post_dict = posts.dict()
    post_dict['id'] = randint(0, 10000000)
    my_posts.append(post_dict)
    return {"data": my_posts}
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

