import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from get_data_from_api import *


## To predict rainfall at next 0, 5, 10, 15, 20, 25, 30 min for all stations
def get_next_30_min_pred(curr_date, curr_time, data, data_pivot, xgboost_model):
    """
    inputs: curr_date, curr_time in string of current time of prediction (to nearest past 5th-min)
    outputs: pandas dataframe with columns (time in min from curr_time, station, predicted_rainfall_value)
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
    df = pd.DataFrame(all_predictions, columns = ['time', 'station', 'prediction'])    
    return df