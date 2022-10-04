
from importlib.metadata import entry_points
from turtle import title
from fastapi import FastAPI 
from fastapi import HTTPException, status, Depends
import psycopg2 # importing psycopg2 to connect with the SQL database
from psycopg2.extras import RealDictCursor
from typing import Optional, List
from . import models,schemas
from .db import engine
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db import get_db
# from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(bind=engine)

app = FastAPI(           
    version= "614-772-8409",
    docs_url= "/",
    title="Rony R. Shabo",
    description="BackEnd Python developer")

# while True:
#     try:
#         conn = psycopg2.connect(host ="localhost", database='my_resume', 
#                                 user='rony', password='Hell33174450$#',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("-----------database connection was successful------------------------")
#         break
#     except Exception as error:
#         print(f"Connection to database failed due to {error} ")
#         time.sleep(2)
        
# for find resume and find index resume, I probebly will delete the hard coded my_resume list of dicts
# and change the source of entries to get it from the DB 



# import os
# # @app.get("/images")
# def images():
#     out = []
#     for filename in os.listdir("./images"):
#         out.append({
#             "name": filename.split(".")[0],
#             "path": "./images/" + filename
#         })
#     return out


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
@app.get("/")
def HTML_Source_code():
    """ Simply referenced to the ("/") directory that referes to the docs_url 
    which is an argument for the fast API implementation Line 13
    
    Please Use the try it out button then Execute"""
    return


# # Personal Image
# app.mount("/static/images", StaticFiles(directory="static"), name="static")
# @app.get("/static/images/Rony Shabo.jpg")
# # @app.get("/static/images/image2.jpg")
# def Images():
    
#     return


#-2- Find all
@app.get("/Resume",  response_model=List[schemas.FullResume])
def get_resume(db: Session = Depends(get_db)):
    """
    purpose: get call for all entries in my resume, 
    
    returns: dict obj
    """
    resume = db.query(models.Model_Resume).all()
    return resume


#-3- Find By {id}
@app.get("/Entry/{id}", response_model=schemas.ResumeResponse)
def get_Entry_by_ID(id: int, db:Session = Depends(get_db)):
    """
    purpose: find a sepecific entry by looking for a specific id that the user provides
    
    returns: a single dict object named an entry
    """
    
    resume = db.query(models.Model_Resume).filter(models.Model_Resume.id == id).first()
    print(resume)
    if not resume:
        print("Entry was not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST       ,
                            detail=f'Entry with id {id} was not found'
                            )
    return  resume


# -4- Add to DB with 
@app.post("/Experiance", status_code=status.HTTP_201_CREATED, response_model=schemas.ResumeResponse)
def create_entry(resume: schemas.ResumeBase, db: Session = Depends(get_db)):
    """
    """
    
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
    if resume.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'resume with id: {id} Does not exist')

    resume.delete(synchronize_session = False)
    db.commit()
    return {"data":"The Entry with id {id} was successfully deleted"}



# -6-
@app.put("/Entry/{id}", response_model=schemas.PutResume)
def update_entry(id:int, updated_resumes:schemas.PutResume, db: Session = Depends(get_db)):
    """
    """
    updated_resume = db.query(models.Model_Resume).filter(models.Model_Resume.id == id)

    resumes = updated_resume.first()

    if resumes == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Work Enty with id: {id} Does not exist')
    
    updated_resume.update(updated_resumes.dict(), synchronize_session=False)

    db.commit()

    return updated_resume.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
