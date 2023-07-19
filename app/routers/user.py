from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from .. import utils
from ..database import engine, get_db

router = APIRouter(
    prefix="/users"
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.userOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #Create the hash of passowrd 

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
@router.get("/{id}", response_model=schemas.userOut)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id :  {id} does not found")
    
    return user
    