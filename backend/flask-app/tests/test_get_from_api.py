import pytest
import pandas as pd
import numpy as np

from get_data_from_api import *

def test_get_current_time():
    curr_date_time = get_curr_date_time()
    assert len(curr_date_time) == 2
    assert type(curr_date_time[0]) == str
    assert type(curr_date_time[1]) == str

def test_get_time_tuples():
    sample_date_time = ('2023-04-14 ', '15:18:33')

    assert len(get_time_tuples(sample_date_time, 6)) == 6
    assert len(get_time_tuples(sample_date_time, 12)) == 12

def test_extract_data():
    sample_timestamps = [('2023-04-14', '15:08:33'),
                         ('2023-04-14', '15:03:33'),
                         ('2023-04-14', '14:58:33'),
                         ('2023-04-14', '14:53:33')]
    timestamps_extracted = sample_timestamps
    url = "https://api.data.gov.sg/v1/environment/rainfall"
    data = extract_data(timestamps_extracted)
    
    assert len(data) == 4

def test_sliding_window():
    data_pivot = get_updated_data_pivot()
    curr_date_time = get_curr_date_time()
    num_stations = len(data_pivot.columns)

    sliding_window = create_sliding_window(curr_date_time, data_pivot)

    assert len(readings[0]) == 109  # each sliding window has 109 columns
    assert len(readings[1]) == 109  # each sliding window has 109 columns
    assert len(readings) == num_stations  # each station has its own sliding window, so total number of sliding windows = num of stations

    assert type(readings[0][0]) == str  # 1st column of each sliding window is station number
    assert type(readings[0][1]) == int  # 2nd column of each sliding window is T1S1_time: time in minute
    assert type(readings[0][2]) == float  # 3rd column of each sliding window is T1S1_dist: distance of S1 from origin station

