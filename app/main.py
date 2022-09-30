
from tkinter import Entry
from turtle import title
from fastapi import FastAPI 
from fastapi import HTTPException, status, Depends
from pydantic import BaseModel
# importing psycopg2 to connect with the SQL database
import psycopg2
from psycopg2.extras import RealDictCursor
import  time
from . import models
from .db import SessionLocal, engine
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI(           
    version= "614-772-8409",
    docs_url= "/",
    title="Rony R. Shabo",
    description="BackEnd Python developer")
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# importing Pydantic and adding this class, 
# in addition to this refrencing this class in the resume call allows it to act like a template
# giving all the warnings if resume call doesn't have the defined catigories, 
# or not the correct data type

class Resume(BaseModel):
    # Defining the Schema "prone to be amended pending on DB"
    id: int
    title: str 
    work_place: str
    skills: str
    time_of_work : str

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
    resume = db.query(models.Resume).all()
    return resume


#-3- Find By {id}
@app.get("/Entry/{id}")
def get_Entry_by_ID(id: int):
    """
    """
    
    cursor.execute(""" SELECT * from my_resume WHERE id= %s """, (str(id),))
    entry_by_id = cursor.fetchone()
    resume = entry_by_id
    if not resume:
        print("Entry was not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST       ,
                            detail=f'Entry with id: {id} was not found'
                            )
    return {"entry_detail": resume}


# -4- Add to DB with 
@app.post("/Experiance", status_code=status.HTTP_201_CREATED)
def create_entry(resume:Resume,db: Session = Depends(get_db)):
    """
    """

    # ---- this is the original method using sql--------
    # cursor.execute(""" INSERT INTO my_resume (id, title, work_place, skills, time_of_work) 
    #                VALUES (%s,%s,%s,%s) RETURNING *
    #                """, 
    #                (resume.id, resume.title, resume.work_place, resume.skills),)
    # new_experiance = cursor.fetchone()
    # conn.commit()

    new_experiance = models.Resume(id = resume.id, title = resume.title, work_place = resume.work_place, skills = resume.skills, time_of_work = resume.time_of_work)
    
    if new_experiance == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'resume with id: {id} Does not exist')
    db.add(new_experiance)
    db.commit()
    db.refresh(new_experiance)
    return {"data":new_experiance}
#title as str, content as str


# -5-
@app.delete("/Entry/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(id:int):
    """
    """
    #find the index in the arry that has the required ID
    cursor.execute(""" DELETE from my_resume WHERE id= %s returning * """, (str(id),))
    delete_entry = cursor.fetchone()
    conn.commit()
    
    # resume = test_resume
    if delete_entry==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'resume with id: {id} Does not exist')

    return {"data":"The Entry with id {id} was successfully deleted"}



# -6-
@app.put("/Entry/{id}")
def update_entry(id:int, resume:Resume):
    """
    """
    
    cursor.execute(""" UPDATE my_resume SET id = %s, title = %s, work_place = %s, skills = %s, time_of_work = %s WHERE id = %s returning * """,
                   (resume.id,resume.title, resume.work_place,resume.skills,resume.time_of_work, str(id)))
    updated_resume = cursor.fetchone()
    conn.commit()
    
    if updated_resume == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'resume with id: {id} Does not exist')
    
    return{"data":updated_resume}
    # To recap: this put function will look for an Id if it doesnt exist, it will throw a 404
    # if it does exist, we will take the data from resumeman and turn it to a dictionary 
    # then add the id to have it built in and replace the resume with index with resume_dict
    

#SQL alchemy test ground
@app.get("/sql")
def test_resume(db: Session = Depends(get_db)):
    """_summary_

    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """

    # the way to do it is
    #  db ogject and here we need to pass in the model, in our case its the resume in model file. (file.class)
    # since we want to query all the entries there we add a . all otherwise we could specify which one we want
    resumes = db.query(models.Resume).all()
    
    return {"data":resumes}