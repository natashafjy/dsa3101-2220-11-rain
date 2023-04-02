import pandas as pd 
import numpy as np
import requests
import random

random.seed(3101)

url = "https://api.data.gov.sg/v1/environment/rainfall?date=2023-03-26"

response = requests.get(url)

# empty lists, should be of len=66 when filled
station_names = []
station_ids = []
latitudes = []
longitudes = []

def parse_station_info():
    if response.status_code == 200:
        data = response.json()
        stations = data['metadata']['stations']
        
        for i in range(len(stations)):
            loc_temp = stations[i]['location']
            latitudes.append(loc_temp['latitude'])
            longitudes.append(loc_temp['longitude'])
            station_names.append(stations[i]['name'])
            station_ids.append(stations[i]['id'])
        
    else:
        print("Error in API request")


parse_station_info()


lat_by7 = np.repeat(latitudes, 7)
long_by7 = np.repeat(longitudes, 7)

time = [5*i for i in range(7)]*len(latitudes)

precip = np.random.uniform(low=0., high=10., size=(len(time),))

prob = [i/10 for i in precip]

wet = np.random.randint(low=0, high=3, size=(len(prob),))

simulated_data = {'latitude': lat_by7, 'longtitude': long_by7, 'time': time, 'precipitation': precip, 'probability': prob, 'wetness': wet}

station_index = np.arange(start = 1, stop = 67, step = 1)
station = np.repeat(station_index, 7)

# Sanity check
# print(len(response.json()['metadata']['stations']) == len(latitudes))
# print(len(time)==len(lat_by7))

df = pd.DataFrame.from_dict(simulated_data)
df['station'] = station # appending a station index col
df.to_csv('data.csv')
