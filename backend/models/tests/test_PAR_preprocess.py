import pandas as pd

raw_data = pd.read_csv("sample_sliding_window_data.csv")

import sys
sys.path.insert(0, "../save_models")
from PassiveAggressiveRegressor import preprocess

def test_cols_removed():
    """
    tests if the columns date, time, station and T{i}S{j}_station number, where 1 <= i <= 6, are removed
    """
    
    processed_data = preprocess(raw_data)
    processed_cols = list(processed_data.columns)
    
    assert not any("station number" in col_name for col_name in processed_cols)
    assert not ("date" in processed_cols)
    assert not ("time" in processed_cols)
    assert not ("station" in processed_cols)

def test_no_NAs():
    
    processed_data = preprocess(raw_data)

    assert not (processed_data.isnull().values.any())

