from datetime import datetime, timedelta
import requests
import pandas as pd
import json
import numpy as np
import xgboost as xgb

### To retrieve data from API and format data to fit into model

## Current date and time
dt_now = datetime.now()
dt_now_str = dt_now.strftime("%Y-%m-%d %H:%M:%S")
current_date_str = dt_now_str[:11]
current_time_str = dt_now_str[11:]

def get_curr_date_time():
    return(current_date_str, current_time_str)


## num  = 6: Get 6 intervals of timestamps for sliding window
## num != 6: Get most recent 12 timestamps in a list of (date, time) tuples
def get_time_tuples(date_time_tuple, num):
	date_str, time_str = date_time_tuple
	datetime_obj = datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M:%S')
	result = []
	if num == 6:
		for i in range(7,13):
			new_datetime_obj = datetime_obj - timedelta(minutes=i*5)
			new_date_str = new_datetime_obj.strftime('%Y-%m-%d')
			new_time_str = new_datetime_obj.strftime('%H:%M:%S')
			result.append((new_date_str, new_time_str))
	else:
		for i in range(2,14):
			new_datetime_obj = datetime_obj - timedelta(minutes=i*5)
			new_date_str = new_datetime_obj.strftime('%Y-%m-%d')
			new_time_str = new_datetime_obj.strftime('%H:%M:%S')
			result.append((new_date_str, new_time_str))
	return result

timestamps_extracted = get_time_tuples((current_date_str, current_time_str), 12)  # timestamps required to be retrieved using API


## retrieve data of most recent 11 rainfall values for all stations and save into dataframe
url = "https://api.data.gov.sg/v1/environment/rainfall"

data_df = []
def extract_data():
    for row in timestamps_extracted:
	    row_dt = row[0] + "T" + row[1]
	    params = {"date_time": row_dt} # YYYY-MM-DD
	    data_dict = requests.get(url, params=params).json()
	    readings_lst = data_dict["items"]
	    readings_df = pd.DataFrame.from_dict(readings_lst)
	    data_df.append(readings_df)
        
extract_data()
data = pd.concat(data_df, ignore_index=True)


## expand dataframe such that each row is date+time and columns are each stations
def spread_column(lst):
   	new_dict = dict()
   	for ddict in lst:
   		new_dict[ddict["station_id"]] = ddict["value"]
   	return new_dict
data["loc_val"] = data["readings"].map(lambda entry: spread_column(entry))
data = data.join(pd.json_normalize(data["loc_val"]))
data = data.drop(columns = ["readings", "loc_val"])

## reshape dataframe such that each row is date+time and one station only, with cols [date, time, station, value]
data = data.melt(id_vars = ["timestamp"], var_name = "station")

## Drop timestamp column and convert to date & time columns
data[['date_time', 'timezone']] = data['timestamp'].str.split('+', expand=True)
data[['date', 'time']] = data['date_time'].str.split('T', expand=True)
data.drop('date_time', axis=1, inplace=True)
data.drop('timezone', axis=1, inplace=True)
data.drop('timestamp', axis=1, inplace=True)

## Shift date & time columns to the first 2 columns
data.insert(0, 'time', data.pop('time'))
data.insert(0, 'date', data.pop('date'))


## Pivot data such that each column is an individual station, with cols [date, time, station S08, S104, S106, ...]
data_pivot = data.pivot(index=["date","time"], columns="station", values="value")


## Load dictionary of 5 nearest stations to each origin station
with open('5-nearest-stations.txt') as f:
    station_dict = f.read()
k_nearest_dic = json.loads(station_dict)

all_stations = list(data_pivot.columns)


## create sliding window data required as input into model for the provided required datetime
def create_sliding_window(req_datetime, rain_data_pivot):
    """
    req_datetime: tuple of only 1 date and 1 time in the form (date, time)
    returns a list of lists of the form [orig_stn, T1S1_time, T1S1_dist, T1S1_value, T1S2_time, ... , T6S6_time, T6S6_dist, T6S6_value] for input into model
    """
    lst_of_rows = []
    orig_date, orig_time = req_datetime
    for orig_stn in all_stations:
        nearest_k_stns = k_nearest_dic[orig_stn]
        newRow = []
        newRow.append(orig_stn)
        # rowIndex = req_datetime.index[i]
        for time_indx,(date,time_stamp) in enumerate(get_time_tuples((orig_date, orig_time), 6),start=1):
            for (stn,dist) in nearest_k_stns:
                newRow.append(-5*time_indx-30)
                newRow.append(dist)
                if rain_data_pivot.get(stn) is None:
                    newRow.append(0.0)
                else:
                    newRow.append(rain_data_pivot.get(stn).get((date,time_stamp)))
            newRow.append(-5*time_indx-30)
            newRow.append(0)
            if rain_data_pivot.get(orig_stn) is None:
                newRow.append(0.0)
            else:
                newRow.append(rain_data_pivot.get(orig_stn).get((date,time_stamp)))
        lst_of_rows.append(newRow)
    return lst_of_rows


## As the 2 most recent readings cannot be retrieved via API call, we need to predict these values and add them into the data
xgboost_model = xgb.XGBRegressor()
xgboost_model.load_model("xgboost_model.json")
## To predict most recent 2 readings first
sec_rec_date = data['date'].max()
sec_rec_time = data['time'].max()
sec_rec_datetime_obj = datetime.strptime(sec_rec_date + ' ' + sec_rec_time, '%Y-%m-%d %H:%M:%S')
sec_rec_datetime_obj = sec_rec_datetime_obj + timedelta(minutes=5)
sec_rec_date_str = sec_rec_datetime_obj.strftime('%Y-%m-%d')
sec_rec_time_str = sec_rec_datetime_obj.strftime('%H:%M:%S')

most_rec_datetime_obj = sec_rec_datetime_obj + timedelta(minutes=5)
most_rec_date_str = most_rec_datetime_obj.strftime('%Y-%m-%d')
most_rec_time_str = most_rec_datetime_obj.strftime('%H:%M:%S')

## 2nd most recent readings
readings = create_sliding_window((sec_rec_date_str, sec_rec_time_str), data_pivot)
for win in readings:
    stn = win[0]
    features = np.array(win[1:])
    features = features.reshape(1, 108)
    pred_rain = xgboost_model.predict(features)
    data.loc[len(data.index)] = [sec_rec_date_str, sec_rec_time_str, stn, pred_rain[0]]

## Most recent readings
readings = create_sliding_window((most_rec_date_str, most_rec_time_str), data_pivot)
for win in readings:
    stn = win[0]
    features = np.array(win[1:])
    features = features.reshape(1, 108)
    pred_rain = xgboost_model.predict(features)
    data.loc[len(data.index)] = [most_rec_date_str, most_rec_time_str, stn, pred_rain[0]]
# update data_pivot with the 2 most recent readings
data_pivot = data.pivot(index=["date","time"], columns="station", values="value")

def get_updated_data():
    return data
def get_updated_data_pivot():
    return data_pivot