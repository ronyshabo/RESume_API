from app import oauth2
from app.db import get_db
from .. import models, schemas, oauth2
from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from typing import List

import logging

logging.basicConfig(
    filename="logs/resume-logs.log",
    level=logging.DEBUG,
    format="%(module)s : %(levelname)s:  %(message)s - : %(asctime)s",
)
router = APIRouter(prefix="/resume", tags=["Resume"])
# # -a-
# @router.get("/")
# def HTML_Source_code():
#     """ Simply referenced to the ("/") directory that referes to the docs_url
#     which is an argument for the fast API implementation Line 13
#     Please Use the try it out button then Execute"""
#     return
# # Personal Image
# app.mount("/static/images", StaticFiles(directory="static"), name="static")
# @app.get("/static/images/Rony Shabo.jpg")
# # @app.get("/static/images/image2.jpg")
# def Images():
#     return
# -1- Find all
@router.get("/Resume", response_model=List[schemas.FullResume])
def get_resume(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    """
    describtion: This call will initially show you My full resume,
        you will be able to add new entries to it. and will be viewing both my entries,
        and everything you do as well

    purpose: get call for all entries in my resume,

    returns: dictionary obj
    """
    current_user_id = current_user.id  # type: ignore
    logging.info(f"current_user_id = current_user.id is{current_user_id}")

    curr_user_posts = (
        db.query(models.Model_Resume)
        .filter(models.Model_Resume.owner_id == current_user_id)
        .all()
    )
    admin_posts = (
        db.query(models.Model_Resume).filter(models.Model_Resume.owner_id == 3).all()
    )
    logging.info("Get call for the resume has been successful")
    resume = admin_posts + curr_user_posts
    return resume


# -2- Find By {id}
@router.get("/Entry/{id}", response_model=schemas.ResumeResponse)
def get_Entry_by_ID(id: int, db: Session = Depends(get_db)):
    """
    purpose: find a sepecific entry by fetching a specific id that the user provides

    dependncy :
    - db session from fastAPI
        app = fastAPI()

    returns: a single dictionary object
    """
    resume = db.query(models.Model_Resume).filter(models.Model_Resume.id == id).first()
    if not resume:
        logging.debug(f"Entry was not found when attempted to get an antry by Id {id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entry with id {id} was not found",
        )

    return resume


# -3- Add to DB with
@router.post(
    "/Experiance",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResumeResponse,
)
def create_entry(
    resume: schemas.ResumeBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    purpose: End point to create an entries in the Resume table.

    dependncy :
    - db session from fastAPI
        app = fastAPI()
    - user ID: validation from Oauth2 and auth.py

    """
    # ** is unpacking the dict
    new_experiance = models.Model_Resume(owner_id=current_user.id, **resume.dict())  # type: ignore
    db.add(new_experiance)
    db.commit()
    db.refresh(new_experiance)

    if new_experiance == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"resume with id: {id} Does not exist",
        )
    logging.info(
        f"A new experiance has been added to the Database by user {current_user}"
    )
    return new_experiance


# title as str, content as str


# -4-
@router.put("/Entry/{id}", response_model=schemas.PutResume)
def update_entry(
    id: int,
    updated_resumes: schemas.PutResume,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    purpose: The ability to amend the information in a specific Entry in the db

    Returns: the updated Entry located by (id)

    Dependency: This endpoint requires the correct log in and the correct authentications

    """
    updated_resume = db.query(models.Model_Resume).filter(models.Model_Resume.id == id)

    resumes = updated_resume.first()

    if resumes == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work Enty with id: {id} Does not exist",
        )
    if resumes.owner_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to Delete this Entry",
        )

    updated_resume.update(updated_resumes.dict(), synchronize_session=False)

    db.commit()
    logging.info(
        f"A successful amend to post {id} has been made by User {current_user}"
    )
    logging.info("testing new revision for heroku")

    return updated_resume.first()


# -5-
@router.delete("/Entry/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Purpose: The ability to Delete an entry that you have entred. No worries it won't delete anything I created.

    Returns: Either a confirmation of the Deletion or an error message that the Id requested was not found

    Dependency: This endpoint requires the correct log in and authentication, requires an ID for a post to be deleted
    """
    resume_query = db.query(models.Model_Resume).filter(models.Model_Resume.id == id)
    resume = resume_query.first()
    if resume == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"resume with id: {id} Does not exist",
        )
    logging.debug(
        "Attempt to delete post with id {id} was unsuccessful {id} Doesn't exist"
    )
    if resume.owner_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to Delete this Entry",
        )
    logging.warning(
        f"The Current user: {current_user} is not authorized to Delete the Entry with id {id} that belongs to {resume.owner_id} "
    )
    resume_query.delete(synchronize_session=False)
    db.commit()
    logging.info(f"Successfully deleted post with id {id}")
    return {"data": "The Entry with id {id} was successfully deleted"}
