from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional  # Needed for Optional
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
import schemas
from database  import engine, SessionLocal, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app=FastAPI()

class Post(BaseModel):
    title: str
    content: str 
    published: bool=True
    #rating: Optional[int]=None

while True:  # To repeatedly try connecting 

    try:
        conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='mk1998', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database Connection was Successful!")
        break

    except Exception as error:
        print("Connecting DataBase Failed")
        print("Error:", error)
        time.sleep(2)

my_posts=[

    {"title":"Title Post One", "content":"Content of Post One", "id":1},
     
    {"title":"Title Post Two", "content":"Content of Post Two", "id":2}
]


def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p
        

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']==id:
            return i


@app.get("/sqlalchemy")
def test_posts(db:Session=Depends(get_db)):
    return{ "status": "success" }






@app.get("/product")
def get_product():
    cursor.execute(""" SELECT * FROM posts """)
    out = cursor.fetchall()
    print(out)
    return{"data": out} 

@app.post("/product", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """,
                   (post.title, post.content))
    new_post =cursor.fetchone()
    conn.commit()
 
    return{"data":new_post} 


@app.get("/product/{id}")
def get_posts(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s""", (str(id)))
    test_post = cursor.fetchone()
    print(test_post)
    if not test_post:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found!! " )
        
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id {id} not found!! "}
    return {"post_detail": test_post }
    
@app.delete("/product/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id:int):
    # Deleting an item in my_post array
    # Find the index in the array that has required ID 
    # my_posts.pop index
    cursor.execute(""" DELETE FROM posts WHERE id=%s returning *""", (str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()
    if deleted_post==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # To get Response code


@app.put("/product/{id}")
def update_post(id:int, post:Post):

    cursor.execute(""" UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING * """,
                   (post.title, post.content, str(id) ))
    updated_post =cursor.fetchone()
    conn.commit()
    
    
    if updated_post==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
   

    return { "data": updated_post}






@app.get("/")
async def root():
    return {"message": "API Configuration"}



@app.get("/posts")
def get_posts():
    return {"data": my_posts}

#@app.post("/posts", status_code=status.HTTP_201_CREATED)
#def create_posts(post:Post ):
#    post_dict = post.dict()
#    post_dict['id']=random.randrange(0,100000)
#    my_posts.append(post_dict)
#
#    return {"data": post_dict}

#@app.post("/createposts")
#def create_posts(payload: dict=Body(...)):
#    print(payload)
#    return {"new_post":f"title: {payload['title']} content: {payload['content']}"}
# 
@app.post("/posts")
def posts(post:Post ):
    print(post)
    print(post.dict())   # To convert pydantic into dictionary
    return {"data": [post.published,  post.title]}



# title str, content str, category, Bool published, 

@app.get("/posts/{id}")  # User gonna input id - PATH PARAMETER
def get_post(id: int,  response:Response):               # Validation to convert to integer
    post= find_post(id)
    if not post:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found!! " )
        
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id {id} not found!! "}
    return {"post_detail": post }


@app.get("/posts/latest")

def get_latest_post():    # Clash between posts/{id}  and this call.  SO ORDERING MATTERS!!! 
    my_posts[len(my_posts)-1]
    return {"detail":posts}



# Delete a post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id:int):
    # Deleting an item in my_post array
    # Find the index in the array that has required ID 
    # my_posts.pop index
    index=find_index_post(id)
    if index==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # To get Response code


class UpdatePost:
    title: str
    content: str 
    published: bool=True
    rating: Optional[int]=None

# Update Post

@app.put("/posts/{id}")
def update_post(id:int, post:Post):

    index=find_index_post(id)
    
    if index==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict

    return { "data": post_dict}








