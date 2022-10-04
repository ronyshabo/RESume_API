
from sqlalchemy import Column, Integer, String
from .db import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Model_Resume(Base):
    __tablename__  = "my_resume"
    
    id = Column(Integer, primary_key = True, nullable = False )
    title = Column(String, nullable = False)
    work_place = Column(String, nullable = False)
    skills = Column(String, nullable = False)
    time_of_work = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False,server_default=text('now()'))


class  User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False )
    email = Column(String, nullable = False, unique =True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False,server_default=text('now()'))
