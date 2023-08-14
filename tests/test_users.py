import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import schemas
from app.config import settings
from app.database import get_db, Base




#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Kcgeraud1986!@localhost:5432/fastapi_test'

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db



@pytest.fixture
def client():
    # Run our code before we run our test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
       

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