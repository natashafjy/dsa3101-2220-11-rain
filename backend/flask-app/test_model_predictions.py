import pytest
import pandas as pd
import numpy as np
import xgboost as xgb

from get_data_from_api import *
from get_next_30_min_pred import *

def test_model_predictions():
    # 1. retrieve data from API and format data to fit into model
    curr_date, curr_time = get_curr_date_time()
    formatted_data = get_updated_data()
    formatted_data_pivot = get_updated_data_pivot()
 
    # 2. use model to generate predictions
    xgboost_model = xgb.XGBRegressor()
    xgboost_model.load_model("xgboost_model.json")
    predicted_data = get_next_30_min_pred(curr_date, curr_time, formatted_data, formatted_data_pivot, xgboost_model)

    assert len(predicted_data.columns) == 3
    assert list(predicted_data.columns) == ['time', 'station', 'value']
    assert predicted_data.time.dtype == 'int64'
    assert predicted_data.station.dtype == object
    assert predicted_data.value.dtype == 'float32'
    assert predicted_data.isnull().values.any() == False

