from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List  # Needed for Optional
import time
import models, schemas, utils
from schemas import UserCreate
from passlib.context import CryptContext
from database  import engine, get_db
from sqlalchemy.orm import Session


# pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")  # Default Hasing Algorithm. # Defined in utils.py

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


@app.get("/posts",  response_model=List[schemas.Post])

def test_posts(db:Session=Depends(get_db), ):

    posts=db.query(models.Post).all()  # Accessing models

    return posts



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id:int, db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id)
    
    if post.first()==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()


@app.put("/posts/{id}")
def update_post(id:int, post:schemas.PostCreate, db:Session=Depends(get_db), response_model=schemas.Post):
    

    post_query=db.query(models.Post).filter(models.Post.id==id) # Find Query to be modified

    post_query_first=post_query.first()      # Find only first query 
    
    if post_query_first==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    

    
    post_query.update(post.dict(), synchronize_session=False) 
    db.commit()
    
    return post_query_first

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)

def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):

    hashed_password=utils.pwd_context.hash(user.password)
    user.password=hashed_password


    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id:int, db:Session=Depends(get_db)):

    user=db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} does not exist")
    
    return user
