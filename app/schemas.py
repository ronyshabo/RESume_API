from datetime import datetime
from pydantic import BaseModel, EmailStr


class ResumeBase(BaseModel):
    title: str 
    work_place: str
    skills: str
    time_of_work : str
    
    

class CreateResume(ResumeBase):
    id: int

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    #pydantic model to reference the orm and activate it
    class Config:
        orm_mode = True

class FullResume(ResumeBase):
    id: int
    created_at :datetime
    owner_id: int

    #pydantic model to reference the orm and activate it
    class Config:
        orm_mode = True

class ResumeResponse(ResumeBase):
    created_at : datetime
    owner_id: int
    
    #pydantic model to reference the orm and activate it
    class Config:
        orm_mode = True

class PutResume(ResumeBase):
    #pydantic model to reference the orm and activate it
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password:str
   

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int