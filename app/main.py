
from fastapi import FastAPI 
# from fastapi.staticfiles import StaticFiles
from .routers import resume,user, auth
from fastapi.middleware.cors import CORSMiddleware


# This command is not needed anymore since it was allowing run create statments for sqlalchemy.
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(           
    version= "614-772-8409",
    docs_url= "/",
    title="Rony R. Shabo",
    description="""
    BackEnd Python developer
    Source Code:        https://github.com/ronyshabo/RESume_API
    Email:              ronyshabbo@gmail.com
    LinkedIn:           https://www.linkedin.com/in/rony-shabo/

    Welcome to my first API, I used my Resume as an example of the things I can perform; in order to be able to view my resume I encurage you to:
        1- Please start by creating a user with the POST command under Users.
        2- Authenticate your user "Log in" in the last endpoint. 
        3- Enter only your email and password in the green Authorize button to the right of the page
        4- My changes are locked and nothing you do would change anything other users did.
        5- Explore it yourself, and most of all enjoy your time my friend
        One last thing.
        6- Any changes you create would be added under your credentials.
           so you will only be able to change / delete your entries. 
    """)
origins=["*"]

app.add_middleware(CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(user.router)
app.include_router(auth.router)

