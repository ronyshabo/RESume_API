from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.db import Base
from app.models import Model_Resume


    # Defining the Schema "prone to be amended pending on DB"


class ResumeBase(BaseModel):
    title: str 
    work_place: str
    skills: str
    time_of_work : str
    
    

class CreateResume(ResumeBase):
    id: int


class FullResume(ResumeBase):
    id: int
    created_at :datetime
    class Config:
        orm_mode = True

class ResumeResponse(ResumeBase):
    created_at : datetime
    
    class Config:
        orm_mode = True

class PutResume(ResumeBase):
    id:int
    
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password:str
   

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]= None