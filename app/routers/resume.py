
from app import oauth2
from app.db import get_db
from .. import models, schemas, oauth2
from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. db import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/resume",
    tags= ["Resume"]
)



# -1-
@router.get("/")
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
@router.get("/Resume",response_model=List[schemas.FullResume])
def get_resume(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    purpose: get call for all entries in my resume, 
    
    returns: dict obj
    """

    resume1 = db.query(models.Model_Resume).filter(models.Model_Resume.owner_id == 8).all()
    resume2 = db.query(models.Model_Resume).filter(models.Model_Resume.owner_id == current_user.id).all()
    resume = resume1 + resume2
    return resume


#-3- Find By {id}
@router.get("/Entry/{id}", response_model=schemas.ResumeResponse)
def get_Entry_by_ID(id: int, db:Session = Depends(get_db)):
    """
    purpose: find a sepecific entry by looking for a specific id that the user provides

    dependncy :
    - db session from fastAPI 
        app = fastAPI()

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
@router.post("/Experiance", status_code=status.HTTP_201_CREATED, response_model=schemas.ResumeResponse)
def create_entry(resume: schemas.ResumeBase,
                db: Session = Depends(get_db), 
                current_user :int= Depends(oauth2.get_current_user)
 ):
    """
    purpose: End point to fetch all entries in the Resume table.

    dependncy :
    - db session from fastAPI 
        app = fastAPI()
    - user ID: validation from Oauth2 and auth.py

    returns:
    full resume 
    
    Notes:
    This function, would foce the user to be logged in first from the Oauth2 folder,

    """
    print(current_user.email)
    # ** is unpacking the dict
    new_experiance = models.Model_Resume(owner_id = current_user.id,**resume.dict())
    db.add(new_experiance)
    db.commit()
    db.refresh(new_experiance)
    
    if new_experiance == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'resume with id: {id} Does not exist')
    return new_experiance
#title as str, content as str


# -5-
@router.put("/Entry/{id}", response_model=schemas.PutResume)
def update_entry(id:int, updated_resumes:schemas.PutResume, 
                db: Session = Depends(get_db), 
                current_user :int= Depends(oauth2.get_current_user)
            ):
    """
     purpose: The ability to adjust the information in a specific Entry in the db

     returns: the Entry located by (id)

    """
    updated_resume = db.query(models.Model_Resume).filter(models.Model_Resume.id == id)

    resumes = updated_resume.first()

    if resumes == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Work Enty with id: {id} Does not exist')
    
    updated_resume.update(updated_resumes.dict(), synchronize_session=False)

    db.commit()

    return updated_resume.first()


# -6-
@router.delete("/Entry/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(id:int, db: Session = Depends(get_db), 
                current_user :int= Depends(oauth2.get_current_user)):
    """
    """
    resume_query = db.query(models.Model_Resume).filter(models.Model_Resume.id == id)
    resume = resume_query.first()
    if resume ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'resume with id: {id} Does not exist')

    if resume.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    resume_query.delete(synchronize_session = False)
    db.commit()
    return {"data":"The Entry with id {id} was successfully deleted"}

