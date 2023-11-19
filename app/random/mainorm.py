from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List  # Needed for Optional
import time
import models
import schemas 
from schemas import PostCreate
from database  import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app=FastAPI()

class Post(BaseModel):
    title: str
    content: str 
    published: bool=True
    #rating: Optional[int]=None






@app.get("/posts",  response_model=List[schemas.Post])

def test_posts(db:Session=Depends(get_db), ):

    posts=db.query(models.Post).all()  # Accessing models

    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)

# Adding response_model=schemas.Post, so that only user information sent are shown and not everything inserted into db 

def create_posts(post:schemas.PostCreate, db:Session=Depends(get_db)):  # importing db is for testing and convinience 

    new_post=models.Post(**post.dict())
    #new_post=models.Post(title=post.title, content=post.content, published=post.published)  
    # Alternate method. Don't get confused with two Post classes. One is of models.py other related to FASTApi 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/posts/{id}")

def get_posts(id:int, db:Session=Depends(get_db), response_model=schemas.Post):
    
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    
    if not post:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found!! " )
        
        
    return  post 
    


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