from app import schemas
from .database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello@gmail.com",
                                       "password": "password123"})
    new_user = schemas.userOut(**res.json())
    print(res.json())
    assert res.status_code == 201