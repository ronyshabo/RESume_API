from jose import JWSError, jwt
from datetime import datetime, timedelta
# Secret key
# Algo
#  Experation time

SECRET_KEY = "a614z772x8409w742v611w118"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINS = 30

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
