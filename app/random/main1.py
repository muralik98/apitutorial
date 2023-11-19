from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional  # Needed for Optional
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
#import models
from database  import engine, SessionLocal, get_db





app=FastAPI()

my_posts=[

    {"title":"Title Post One", "content":"Content of Post One", "id":1},
     
    {"title":"Title Post Two", "content":"Content of Post Two", "id":2}
]


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
        time.sleep(2)   # Gives a pause of 2second before retrying 

# ---------------------------------------------------------------------------------------
# Custom Functions 

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p


# --------------------------

@app.get("/posts")

def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts=cursor.fetchall()

    return {"data":posts}



@app.post("/posts", status_code=status.HTTP_201_CREATED)

def get_posts(post:Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    new_post=cursor.fetchone()
    conn.commit()           # Important to save
    return {"data":new_post}

# We can use f-string bu then vulnerable to SQL injection

@app.get("/posts/{id}")

def get_posts(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id),))  # Since select statement is string id should also be string   
    post=cursor.fetchone()
    
    if not post:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found!! " )
        
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id {id} not found!! "}
    return {"post_detail": post }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id=%s returning *""", (str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()
    if deleted_post==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    

@app.put("/posts/{id}")
def update_post(id:int, post:Post):

    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
                   (post.title, post.content, post.published, str(id) ))
    updated_post =cursor.fetchone()
    conn.commit()
    
    if updated_post==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    return { "data": updated_post}