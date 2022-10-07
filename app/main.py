
from fastapi import FastAPI 
from . import models
from .db import engine
# from fastapi.staticfiles import StaticFiles
from .routers import resume,user, auth
models.Base.metadata.create_all(bind=engine)

app = FastAPI(           
    version= "614-772-8409",
    docs_url= "/",
    title="Rony R. Shabo",
    description="BackEnd Python developer")

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


app.include_router(resume.router)
app.include_router(user.router)
app.include_router(auth.router)