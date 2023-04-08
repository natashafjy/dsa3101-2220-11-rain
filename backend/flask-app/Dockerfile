FROM python:3.10.6-slim-buster

## Add Python script, requirements file and templates folder to /app 
## directory on the image:
WORKDIR /app

COPY backend.py backend.py
COPY init_db.py init_db.py
COPY requirements.txt requirements.txt
# COPY init_db.sql /docker-entrypoint-initdb.d/init_db.sql

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

## Set the environment variable for the flask application here:
ENV FLASK_APP backend
ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
