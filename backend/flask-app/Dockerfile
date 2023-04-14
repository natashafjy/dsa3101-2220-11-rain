FROM python:3.10.6-slim-buster

## Add Python script, requirements file and templates folder to /app 
## directory on the image:
WORKDIR /app

COPY data data
COPY backend.py backend.py
COPY requirements.txt requirements.txt
COPY get_routine_rain_probability.py get_routine_rain_probability.py
COPY get_last_rain.py get_last_rain.py
COPY 5-nearest-stations.txt 5-nearest-stations.txt
COPY get_data_from_api.py get_data_from_api.py
COPY get_next_30_min_pred.py get_next_30_min_pred.py
COPY xgboost_model.json xgboost_model.json

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

## Set the environment variable for the flask application here:
ENV FLASK_APP backend
ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
