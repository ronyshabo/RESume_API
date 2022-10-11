from jose import JWTError, jwt
from datetime import datetime, timedelta
from .config import settings
from app import models
from . import schemas, db 
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oausth2_scheme = OAuth2PasswordBearer(tokenUrl='Login')

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = settings.access_token_expire_time)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_access_token(token:str, credentials_exception):
    """
    Summary: 
    Decode the token, we extract the Id from Payload otherwise Throw an Error

    Returns:
    Token Data: that is the ID
    """
    try:
        payload=jwt.decode(token,settings.secret_key, algorithms=[settings.algorithm])
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token_data: str = Depends(oausth2_scheme), db: Session = Depends(db.get_db)):
    """
    summary:
    a function to varify the access token by passing the token taken from the User

    Returns:
        _type_: token object 
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Couldn't validate Credentials", 
        headers={"WWW-Authentiacte":"Bearer"}
        )

    token_data = verify_access_token(token_data, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user