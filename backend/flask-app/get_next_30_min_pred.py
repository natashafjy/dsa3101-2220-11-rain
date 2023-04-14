import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from get_data_from_api import *


## To predict rainfall at next 0, 5, 10, 15, 20, 25, 30 min for all stations
def get_next_30_min_pred(curr_date, curr_time, data, data_pivot, xgboost_model):
    """
    This function returns the predicted rainfall values at all stations for 
    time = 0, 5, 10, 15, 20, 25, 30 minutes after current time of prediction (to nearest past 5th-min).

    Args: 
        curr_date (str): Date in string of current time of prediction (to nearest past 5th-min)
        curr_time (str): Timestamp in string of current time of prediction (to nearest past 5th-min)
        data (pandas Dataframe): rainfall data for all stations from the past 1hr 10min at 5-min interval 
                                 in pandas Dataframe with columns date, time, station, value
        data_pivot (pandas Dataframe): pivoted data from data with each station as its own column and date, time as rows
    
    Returns:
        pandas Dataframe with columns containing time in min from curr_time, station, predicted_rainfall_value
        with column names time, station, value
    """
    all_predictions = []
    curr_dt_obj = datetime.strptime(curr_date + ' ' + curr_time, '%Y-%m-%d %H:%M:%S')
    for t in range(0, 7):
        next_dt_obj = curr_dt_obj + timedelta(minutes=t*5)
        next_date_str = next_dt_obj.strftime('%Y-%m-%d')
        next_time_str = next_dt_obj.strftime('%H:%M:%S')

        readings = create_sliding_window((next_date_str, next_time_str), data_pivot)
        for win in readings:
            stn = win[0]
            features = np.array(win[1:])
            features = features.reshape(1, 108)
            pred_rain = xgboost_model.predict(features)
            stn_pred = [t*5, stn, pred_rain[0]]
            all_predictions.append(stn_pred)
    df = pd.DataFrame(all_predictions, columns = ['time', 'station', 'value'])    
    return df