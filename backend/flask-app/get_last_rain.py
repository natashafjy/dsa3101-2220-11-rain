import pandas as pd
import requests
from datetime import date, timedelta, datetime
import pykrige
import numpy as np

def get_last_rain(points_of_interest):
    """
    input: 
        (lst) points_of_interest: (longitude, latitude) of the start and end points on the user's running route 
    output:
        (int) last_rain_start and (int) last_rain_end: number of minutes since last rain (>=0.1mm) observed at the start and end points 
    """
    today = date.today() # YYYY-MM-DD
    yesterday = today - timedelta(1)

    url = "https://api.data.gov.sg/v1/environment/rainfall"

    def spread_column(lst):
        new_dict = dict()
        for ddict in lst:
            new_dict[ddict["station_id"]] = ddict["value"]
        return new_dict

    # obtain rainfall data from yesterday
    if int(datetime.now().strftime("%H")) <= 1:
        # if time is earlier than 2am, we will need to check the previous day's data in order to get 2 hours' worth of data
        yesterday = today - timedelta(1)
        params = {"date": yesterday}
        data_dict = requests.get(url, params=params).json()

        ytd_readings_lst = data_dict["items"]
        ytd_readings_df = pd.DataFrame.from_dict(ytd_readings_lst)
        ytd_readings_df["loc_val"] = ytd_readings_df["readings"].map(lambda entry: spread_column(entry))
        ytd_readings_df = ytd_readings_df.join(pd.json_normalize(ytd_readings_df["loc_val"]))

    # obtain rainfall data from today
    params = {"date": today}
    data_dict = requests.get(url, params=params).json()

    readings_lst = data_dict["items"]
    readings_df = pd.DataFrame.from_dict(readings_lst)
    readings_df["loc_val"] = readings_df["readings"].map(lambda entry: spread_column(entry))
    readings_df = readings_df.join(pd.json_normalize(readings_df["loc_val"]))

    # combine 2 days of data if it is earlier than 2am
    if int(datetime.now().strftime("%H")) <= 1:
        readings_df = pd.concat([ytd_readings_df, readings_df], ignore_index=True)

    # obtain data up to 2 hours ago
    last_2_hours = readings_df.tail(23) 

    last_2_hours.reset_index(drop=True, inplace=True)

    last_2_hours["idx"] = last_2_hours.index
    last_2_hours["mins_ago"] = 120 - 5 * last_2_hours["idx"]

    last_2_hours.drop(columns=["timestamp", "readings", "loc_val", "idx"], inplace=True)

    # find rows (ie timestamps) where there is rain (to reduce number of timestamps we need to krige and check)
    last_2_hours['sum'] = last_2_hours.drop('mins_ago', axis=1).sum(axis=1)
    last_2_hours = last_2_hours[last_2_hours["sum"] > 0]

    # sorted list of mins_ago with non-zero rain
    has_rain = sorted(list(set(last_2_hours["mins_ago"]))) 

    # drop "sum" row and melt, so df has the columns ["mins_ago", "station", "value"]
    last_2_hours = last_2_hours[last_2_hours["sum"] > 0].drop('sum', axis=1)
    df = pd.melt(last_2_hours, id_vars="mins_ago", var_name="station")

    # import station data and merge with df
    station_data = pd.read_csv("data/station_data.csv", index_col = 0, dtype = {"device_id":"string", "name":"string", "latitude":"float64", "longitude":"float64"})
    data = df.merge(station_data, left_on="station", right_on="device_id")

    # initialise values as 125 (>120 mins, hence outside the range of possible values of mins_ago)
    last_rain_start = 125
    last_rain_end = 125

    for time_ago in has_rain:

        # if last_rain_start and last_rain_end have been set with values, 
        # then can break early since mins_ago would be larger than the current values
        if last_rain_start < 125 and last_rain_end < 125:
            break 

        # filter to get data at particular time
        data_at_time = data[data["mins_ago"] == time_ago].dropna()

        x = np.array(data_at_time["longitude"])
        y = np.array(data_at_time["latitude"])
        z = np.array(data_at_time["value"])

        ordinary_kriging = pykrige.OrdinaryKriging(x, y, z)
        
        # point_num = 0 --> start_point;  point_num = 1 --> end_point
        for point_num in range(len(points_of_interest)):

            point_long, point_lat = points_of_interest[point_num][0], points_of_interest[point_num][1]

            # form grid of values around point
            gridx = np.arange(point_long-0.005, point_long+0.005, 0.001, dtype = "float64")
            gridy = np.arange(point_lat-0.005, point_lat+0.005, 0.001, dtype = "float64")

            # obtain predicted values and their variances using kriging
            zstar, ss = ordinary_kriging.execute("grid", gridx, gridy)

            zstar_clipped = zstar.clip(0) # replace negative values with 0 
            zstar_1d = zstar_clipped.ravel()
            
            rain_value = np.mean(zstar_1d)

            if point_num == 0:
                if last_rain_start == 125: # last_rain at start point is not recorded yet
                    if rain_value >= 0.1:
                        last_rain_start = time_ago

            if point_num == 1:
                if last_rain_end == 125: # last_rain at end point is not recorded yet
                    if rain_value >= 0.1:
                        last_rain_end = time_ago
    
    return last_rain_start, last_rain_end

def print_example():
    points_of_interest = [(104.78150, 1.29230), (103.80389, 1.26472)]
    print(get_last_rain(points_of_interest))

# print_example()



