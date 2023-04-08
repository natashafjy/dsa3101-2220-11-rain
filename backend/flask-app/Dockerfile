FROM python:3.10.6-slim-buster

## Add Python script, requirements file and templates folder to /app 
## directory on the image:
WORKDIR /app

COPY backend.py backend.py
COPY requirements.txt requirements.txt
COPY get_rain_probability.py get_rain_probability.py
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

## Set the environment variable for the flask application here:
ENV FLASK_APP backend
ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
