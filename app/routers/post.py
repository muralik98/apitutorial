import models, schemas, oauth
from database import get_db
from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func 
from typing import List, Optional  # Needed for Optional


router=APIRouter(
    prefix="/posts", tags=['Posts']        
)           # No need to add /posts in @router methods
            # tags - for better documentation in docs

@router.get("/", response_model=List[schemas.PostOut])

def get_posts( db:Session=Depends(get_db), response_model=schemas.Post, current_user: int = Depends(oauth.get_current_user), limit:int=5, skip:int=0,
              search:Optional[str]=""):

    #post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(post)


    #results=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #print("******",results)

        
    return  posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)



# Adding response_model=schemas.Post, so that only user information sent are shown and not everything inserted into db 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
   
    print(current_user)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



@router.get("/{id}")

def get_posts(id:int, db:Session=Depends(get_db), response_model=schemas.Post, current_user: int = Depends(oauth.get_current_user)):
    
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    
    if not post:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found!! " )
    
    if post.owner_id!= current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Forbidden!!: Not Authorized to perform Request!")
        
        
    return  post 
    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id:int, db:Session=Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id) # Find Query to be modified

    post_query_first=post_query.first()      # Find only first query 
    
    if post_query_first==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    

    if post_query_first.owner_id!= current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Forbidden!!: Not Authorized to perform Request!")
    
    post_query_first.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}")
def update_post(id:int, post:schemas.PostCreate, db:Session=Depends(get_db), response_model=schemas.Post, current_user: int = Depends(oauth.get_current_user)):
    

    post_query=db.query(models.Post).filter(models.Post.id==id) # Find Query to be modified

    post_query_first=post_query.first()      # Find only first query 
    
    if post_query_first==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    if post_query_first.owner_id!= current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Forbidden!!: Not Authorized to perform Request!")
    

    
    post_query.update(post.dict(), synchronize_session=False) 
    db.commit()
    
    return post_query_first