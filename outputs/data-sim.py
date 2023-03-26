import pandas as pd 
import numpy as np
import requests
import random

random.seed(3101)

url = "https://api.data.gov.sg/v1/environment/rainfall?date=2023-03-26"

response = requests.get(url)

latitudes = []
longitudes = []

# updates the latitudes and longitudes of all stations into 2 lists
def get_stations_lat_long():
    if response.status_code == 200:
        data = response.json()
        stations = data['metadata']['stations']
        
        for i in range(len(stations)):
            loc_temp = stations[i]['location']
            latitudes.append(loc_temp['latitude'])
            longitudes.append(loc_temp['longitude'])
    else:
        print("Error in API request")


get_stations_lat_long()

lat_by7 = np.repeat(latitudes, 7)
long_by7 = np.repeat(longitudes, 7)

time = [5*i for i in range(7)]*len(latitudes)

precip = np.random.uniform(low=0., high=10., size=(len(time),))

prob = [i/10 for i in precip]

wet = np.random.randint(low=0, high=3, size=(len(prob),))

simulated_data = {'latitude': lat_by7, 'longtitude': long_by7, 'time': time, 'precipitation': precip, 'probability': prob, 'wetness': wet}

# Sanity check
# print(len(response.json()['metadata']['stations']) == len(latitudes))
# print(len(time)==len(lat_by7))

df = pd.DataFrame.from_dict(simulated_data)

df.to_csv('outputs/data.csv')