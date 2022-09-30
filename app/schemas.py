from msilib.schema import Class
from pydantic import BaseModel


    # Defining the Schema "prone to be amended pending on DB"


class ResumeBase(BaseModel):
    id: int
    title: str 
    work_place: str
    skills: str
    time_of_work : str

class ResumeCreate(ResumeBase):
    pass

