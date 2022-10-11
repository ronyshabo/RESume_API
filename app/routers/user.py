from app.db import get_db
from .. import models, schemas,utils
from fastapi import status, Depends, APIRouter, HTTPException
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
    # -1- created  the hashed version of pwad when createing the user
        #  this will link to utils and hash the password

    # Hash the password that is retrieved from user.password
    hased_password = utils.hash(user.password)
    user.password = hased_password

    new_user = models.User(**user.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/user/{id}",response_model = schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() 

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f"User with id {id} not found")
    return user