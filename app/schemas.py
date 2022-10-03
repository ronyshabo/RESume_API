from datetime import datetime
from msilib.schema import Class
from pydantic import BaseModel

from app.db import Base
from app.models import Model_Resume


    # Defining the Schema "prone to be amended pending on DB"


class ResumeBase(BaseModel):
    id: int
    title: str 
    work_place: str
    skills: str
    time_of_work : str

class ResumeCreate(BaseModel):
    title: str 
    work_place: str
    skills: str
    time_of_work : str



class ResumeResponse(BaseModel):
    title: str 
    work_place: str
    skills: str
    time_of_work : str
    created_at : datetime
    class Config:
        orm_model = True