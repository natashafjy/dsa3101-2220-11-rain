import pandas as pd
import numpy as np
import xgb
from sklearn.neural_network import MLPRegressor

# to import from other folders?
import sys
sys.path.insert(0, "../models/save_models")

from MLPRegressor import evaluate


def test_xgb_model_metrics():
    xgboost_model = xgb.XGBRegressor()
    model = xgboost_model.load_model("models/save_models/xgboost_model.pkl")

    ## not practical to test by using the model to predict? will need to generate fake training data (or read_csv?)
    
    rates = evaluate(y_pred, y_true)


    assert # rates >= [0, 0, 0] 
    

def test_mlp_model_metrics():
    regression_model = MLPRegressor()
    model = regression_model.load_model("models/save_models/MLPRegressor.pkl")