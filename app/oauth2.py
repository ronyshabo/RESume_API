from jose import JWSError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oausth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# Secret key
# Algo
#  Experation time

SECRET_KEY = "A614z772X8409w742V611W118"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINS = 30

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str, credentials_exception):
    """
    Summary: 
    Decode the token, we extract the Id from Payload otherwise Throw an Error

    Returns:
    Token Data: that is the ID
    """
    try:
        payload=jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWSError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oausth2_scheme)):
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

    return verify_access_token(token, credentials_exception)