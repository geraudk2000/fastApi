from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()

#test the data send to API
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post.title)
    return {"data": new_post}
# title str, content str,