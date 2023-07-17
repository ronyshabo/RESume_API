# RESume_API
My personal resume in a RESTful API based on FastAPI and Sqlalchemy


# Welcome to my first full standalone project.
I will demonstrate the fully functioning API I am building using FastAPI 
in addition I am connecting it to SQLalchecmy database

To start make sure you set Up ssh correctly then clone the repo.
Most importantly don't forget to CD into the correct directory.
* always start by updating pip
   $ python -m pip install --upgrade pip

1- make sure you have the venv initalized then activated
   $ pip install virtualenv
   $ python -m venv api_venv

   To Activate api_venv was used as a name and so activating it becomes:
   $ source api_venv/scripts/activate
   
2- Dependencies will be available after 
   $ pip install -r requirements.txt
   - I personally had problems with dateutil when working on alembic
   $ pip install python-dateutil --upgrade

3- setup a .env file inside your API directory. and provice the following values
   Those variables will be migrating to SQLALCHEMY_DATABASE_URL in db.py .However,
   these vairables will be going through config.py first to be checked and verified
   DB_HOSTNAME=localhost
   DB_PORT= By default postgress chose 5432 I kept it that way for myself
   DB_PASSWORD= 
   DB_NAME=
   DB_USERNAME="by default postgress sets it as postgress"
   
   SECRET_KEY=find a secret Key and this would be yours to keep secure
   ALGORITHM="Type of Algorithm you would prefer to you. HS256 is my personal choice"
   ACCESS_TOKEN_EXPIRE_TIME="Per Minutes","This will decide how many mins the session for each log in"

4- setup Uvicorn, then run locally 
   $ pip install uvicorn
   
   Run Uvicorn locally using
   $ uvicorn app.main:app --reload
   
   * this --reload flag helps your application update and run everytime you do a change, 
  and it reflects directly to the API

   keep in mind that main.py has been migrated to app directory
   Hense the app.main:app command
