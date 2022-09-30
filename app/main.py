
from multiprocessing import synchronize
from telnetlib import SE
from tkinter import Entry
from turtle import title
from fastapi import FastAPI 
from fastapi import HTTPException, status, Depends

# importing psycopg2 to connect with the SQL database
import psycopg2
from psycopg2.extras import RealDictCursor
import  time
from . import models,schemas
from .db import engine
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db import get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(           
    version= "614-772-8409",
    docs_url= "/",
    title="Rony R. Shabo",
    description="BackEnd Python developer")
        
# importing Pydantic and adding this class, 
# in addition to this refrencing this class in the resume call allows it to act like a template
# giving all the warnings if resume call doesn't have the defined catigories, 
# or not the correct data type



# here we are using the conn to establish a connection and the required arguments are important
# this  is a bad example since the passwords and the host are just there with the code
# TODO for later
while True:
    try:
        conn = psycopg2.connect(host ="localhost", database='my_resume', 
                                user='rony', password='Hell33174450$#',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("-----------database connection was successful------------------------")
        break
    except Exception as error:
        print(f"Connection to database failed due to {error} ")
        time.sleep(2)
        
        

my_resumes = [{
             "id":1, 
             "title":"Network Engineer I ",
             "work_place":"Charter Communications, Spectrum Enterprise ",
             "time_of_work":"02/2022 ->  Present", 
             "skills":
                """-1- Installation and maintenance of network communications 
                -2- Configure various network devices and services (Adva, Cisco, Junipor, Rad) 
                -3- Orchestrate the underlying physical infrastructure of the overlay networks 
                -4- Experience with data modeling, data architecture, and query creation for relational and transactional database or database solutions 
                -5- Develop, test, improve, and document the software supporting data acquisition processes"""
},
            {
            "id":2, 
            "title":"Service Reliability Engineer",
            "work_place":"Charter Communications, Collabera ",
            "time_of_work":"12/2021 ->  02/2022", 
            "skills":
            """-1-Build microservices, and shared components using REST APIs using Flask
                -2-Utilize automation and containerization technologies with Ansible, and Docker for automation and containerization
                -3-Optimize SQL queries for the heavy-load parts of our databases
"""}]

def find_resume(id):
    """ Auxilary Functions to help make sure to find the {id} and the index
    for the search query  """
    for p in my_resumes:
        if p["id"] == id:
            return p
        
def find_index_resume(id):
    for i, p in enumerate(my_resumes):
        if p['id'] ==id:
            return i
    


# -1-
# Path worktime_of_works AKA route
@app.get("/")
def HTML_Source_code():
    """ Simply referenced to the ("/") directory that referes to the docs_url 
    which is an argument for the fast API implementation Line 13
    
    Please Use the try it out button then Execute"""
    return



#-2- Find all
@app.get("/resume")
def get_resume(db: Session = Depends(get_db)):
    """
    """

    # # here  you use cursor.excute and pass in the SQL statment
    # cursor.execute(""" SELECT * FROM my_resume
    #                         ORDER BY id ASC""")
    # resume =cursor.fetchall()

    resume = db.query(models.Model_Resume).all()
    # To find the right way to order them 
    return resume


#-3- Find By {id}
@app.get("/Entry/{id}")
def get_Entry_by_ID(id: int, db:Session = Depends(get_db)):
    """
    """
    
    resume = db.query(models.Model_Resume).filter(models.Model_Resume.id == id).first()
    print(resume)
    if not resume:
        print("Entry was not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST       ,
                            detail=f'Entry with id: {id} was not found'
                            )
    return  resume


# -4- Add to DB with 
@app.post("/Experiance", status_code=status.HTTP_201_CREATED)
# -------------------| here
def create_entry(resume:schemas.ResumeCreate, db: Session = Depends(get_db)):
    """
    """

    # ---- this is the original method using sql--------
    # cursor.execute(""" INSERT INTO my_resume (id, title, work_place, skills, time_of_work) 
    #                VALUES (%s,%s,%s,%s) RETURNING *
    #                """, 
    #                (resume.id, resume.title, resume.work_place, resume.skills),)
    # new_experiance = cursor.fetchone()
    # conn.commit()

    # ** is unpacking the dict
    new_experiance = models.Model_Resume(**resume.dict())
    print(new_experiance)
    db.add(new_experiance)
    db.commit()
    db.refresh(new_experiance)
    
    if new_experiance == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'resume with id: {id} Does not exist')
    return new_experiance
#title as str, content as str


# -5-
@app.delete("/Entry/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(id:int, db: Session = Depends(get_db)):
    """
    """
    resume = db.query(models.Model_Resume).filter(models.Model_Resume.id == id)
    # resume = test_resume
    if resume.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'resume with id: {id} Does not exist')

    resume.delete(synchronize_session = False)
    db.commit()
    return {"data":"The Entry with id {id} was successfully deleted"}



# -6-
@app.put("/Entry/{id}")
def update_entry(id:int, updated_resumes:schemas.ResumeCreate, db: Session = Depends(get_db)):
    """
    """
    updated_resume = db.query(models.Model_Resume).filter(models.Model_Resume.id == id)

    resumes = updated_resume.first()

    if resumes == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'resume with id: {id} Does not exist')
    
    updated_resume.update(updated_resumes.dict(), synchronize_session=False)

    db.commit()

    return updated_resume.first()
