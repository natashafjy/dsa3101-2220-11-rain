FROM python:3.9-slim-buster

## Add Python script, requirements file and templates folder to /app 
## directory on the image:
WORKDIR /app

# COPY backend.py backend.py
COPY requirements.txt requirements.txt
COPY data data
COPY apps apps
copy assets assests
COPY app.py app.py
COPY flask_app.py flask_app.py
COPY get_routine_rain_probability.py get_routine_rain_probability.py
COPY get_last_rain.py get_last_rain.py
COPY get_island_rain_probability.py get_island_rain_probability.py
COPY index.py index.py
COPY 5-nearest-stations.txt 5-nearest-stations.txt
COPY get_data_from_api.py get_data_from_api.py
COPY get_next_30_min_pred.py get_next_30_min_pred.py
COPY xgboost_model.json xgboost_model.json
COPY data.csv data.csv

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        make \
        libc-dev \
        python3-dev
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

## Set the environment variable for the flask application here:
ENV FLASK_APP flask_app
# ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT [ "python", "-u", "index.py"]