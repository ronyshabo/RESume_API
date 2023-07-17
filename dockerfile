FROM python:3-alpine3.15
WORKDIR /Resume_Api
COPY . /Resume_Api
RUN pip install -r requirements.txt
# install everything from the requirements
EXPOSE 5432 
# 5432 is the port
CMD python -m uvicorn app.main:app --reload
# our runner

# CMD python ./index.py
# index is the runner 