FROM python:3.10.6-slim-buster

## Add Python script, requirements file and templates folder to /app 
## directory on the image:
WORKDIR /app

# COPY backend.py backend.py
COPY requirements.txt requirements.txt
COPY get_rain_probability.py get_rain_probability.py
COPY data data
COPY apps apps
copy assets assests
COPY app.py app.py
COPY flask_app.py flask_app.py
COPY get_rain_probability.py get_rain_probability.py
COPY get_last_rain.py get_last_rain.py
COPY get_island_rain_probability.py get_island_rain_probability.py
COPY index.py index.py

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

## Set the environment variable for the flask application here:
ENV FLASK_APP flask_app
# ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT [ "python", "-u", "-m", "index.py"]