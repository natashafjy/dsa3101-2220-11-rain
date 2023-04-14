
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from csv import writer

def preprocess_data(save_data = True):
    """

    Converts a dataframe of stations and their corresponding rain values at a particular time into 
    a new dataframe containing the date, time, (target) station, rainfall value, and 
    the 6 nearest stations (including itself) with:
        - their corresponding distances from the target station, 
        - their rainfall values at a particular time,
        - the time relative to the prediction value
        in 5 minute intervals over a 30 mins duration

    Args:
        save_data (default value = True): whether to write data to a csv file named "sliding_window_data.csv"
    Returns:
        None
    """

    station_latlong = pd.read_csv("station_data.csv",index_col=0)
    station_latlong = station_latlong[['device_id','latitude','longitude']]
    station_latlong_dic = station_latlong.set_index('device_id').T.to_dict('list')
    station_latlong_dic = {tuple(v):k for k,v in station_latlong_dic.items()}

    all_latlong = list(station_latlong_dic.keys())

    def find_k_nearest(src, latlongs, k):
        """
        Args:
            src: source station
            latlongs: list of all (latitude, longitude) tuples of station locations
            k: number of nearest stations to return

        Return:
            sorted list containing k (latitude, longitude, distance) tuples, representing the k stations nearest to the source station
        """
        def euclidean_dist(p1,p2):
            return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2
        all_distances = [ (coord[0],coord[1], euclidean_dist(src,coord)) for coord in latlongs]
        return sorted(all_distances, key= lambda x:x[2])[1:k+1] #skips 1st point which is itself


    k_nearest_dic = {}

    # finds the k nearest stations for all stations
    for coord, stn in station_latlong_dic.items():
        k_nearest_dic[stn] = list(map(lambda x: (station_latlong_dic[x[:2]],x[2]), find_k_nearest(coord, all_latlong, 5) ))


    rain_data = pd.read_csv("rain_data_full.csv", index_col=0)

    rain_data_pivot = rain_data.pivot(index=["date","time"], columns="station", values="value")

    rain_data_pivot = rain_data_pivot.to_dict('index')


    def get_time_tuples(date_time_tuple):
        date_str, time_str = date_time_tuple
        datetime_obj = datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M:%S')
        result = []
        for i in range(7,13):
            new_datetime_obj = datetime_obj - timedelta(minutes=i*5)
            new_date_str = new_datetime_obj.strftime('%Y-%m-%d')
            new_time_str = new_datetime_obj.strftime('%H:%M:%S')
            result.append((new_date_str, new_time_str))
        return result


    header = ["date", "time", "station", "value"]
    for time_indx in range(1,7):
        for stn_indx in range(1,7):
            header.append(f'T{time_indx}S{stn_indx}_time')
            header.append(f'T{time_indx}S{stn_indx}_station number')
            header.append(f'T{time_indx}S{stn_indx}_dist')
            header.append(f'T{time_indx}S{stn_indx}_value')

    if save_data is True:
        with open('sliding_window_data.csv',"a", encoding='utf-8', newline='') as file:
            writer_object = writer(file)
            writer_object.writerow(header)
            file.close()

    lst_of_rows = []
    for i in range(1,len(rain_data)):
        orig_date, orig_time, orig_stn, orig_val = rain_data.iloc[i,0], rain_data.iloc[i,1], rain_data.iloc[i,2], rain_data.iloc[i,3]
        nearest_k_stns = k_nearest_dic[orig_stn]
        newRow = [orig_date, orig_time, orig_stn, orig_val]
        # rowIndex = rain_data.index[i]
        for time_indx,(date,time_stamp) in enumerate(get_time_tuples((orig_date, orig_time)),start=1):
            for (stn,dist) in nearest_k_stns:
                newRow.append(-5*time_indx-30)
                newRow.append(stn)
                newRow.append(dist)
                newRow.append(rain_data_pivot.get((date,time_stamp),{}).get(stn,np.nan))
            newRow.append(-5*time_indx-30)
            newRow.append(orig_stn)
            newRow.append(0)
            newRow.append(rain_data_pivot.get((date,time_stamp),{}).get(orig_stn,np.nan))
        lst_of_rows.append(newRow)
        if i % 10000 == 0:
            if save_data is True:
                with open('sliding_window_data.csv',"a", encoding='utf-8', newline='') as file:
                    writer_object = writer(file)
                    writer_object.writerows(lst_of_rows)
            lst_of_rows = []

    if save_data is True:
        #write last batch
        with open('sliding_window_data.csv',"a", encoding='utf-8', newline='') as file:
            writer_object = writer(file)
            writer_object.writerows(lst_of_rows)



