from app.db import get_db
from .. import models, schemas,utils
from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(
    prefix="/users",
    tags= ["Users"]
)

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    '''
    You can add any number of users with a working password.
    The password then hashed and Saved

    and you can use those logins to log in again even if you used it here only
    '''
        # Hash the password -user.password
    hased_password = utils.hash(user.password)
    user.password = hased_password

    new_user = models.User(**user.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
