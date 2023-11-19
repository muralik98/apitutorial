from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session       
from fastapi.security.oauth2 import OAuth2PasswordRequestForm              
import database, schemas, models, utils, oauth  

router=APIRouter(tags=['Authentication'])


# def login(user_credentials:schemas.UserLogin, db:Session=Depends(database.get_db)):


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = oauth.create_access_token(data={"user_id": user.id, "user_email":user.email})


    

    return {"access_token":access_token,  "token_type":"bearer"}

