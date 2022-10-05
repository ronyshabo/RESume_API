from statistics import mode
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import db, schemas, models, utils, oauth2


router = APIRouter(tags=["Authentication"])

@router.post('/Login')
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(db.get_db)):


    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail=f"invalid access")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail=f"invalid access")

    #CREATE A TOKEN
    #RETURN THE TOKEN
    access_token = oauth2.create_access_token(data= {"user_id":user.id})

    return{"access_token":access_token, "token_type":"bearer"}
