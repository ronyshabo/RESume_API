
from fastapi import FastAPI 
from . import models
from .db import engine
# from fastapi.staticfiles import StaticFiles
from .routers import resume,user, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(           
    version= "614-772-8409",
    docs_url= "/",
    title="Rony R. Shabo",
    description="BackEnd Python developer")

app.include_router(resume.router)
app.include_router(user.router)
app.include_router(auth.router)

