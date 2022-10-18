    
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")
    
def hash(password: str):    
    hashed = pwd_context.hash(password)

    return hashed

# hash is only a one way that is why we need the hashed password in our db, 
# and then hash the second log in pwd and they should match
def verify(plain_password, hashed_password):

    return pwd_context.verify(plain_password,hashed_password)