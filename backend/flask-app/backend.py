from flask import Flask
import xgboost as xgb
from get_rain_probability import *

app = Flask(__name__)

@app.route("/")
def login():
    '''
    To be implemented
    '''
    pass

@app.route("/signup")
def sign_up():
    '''
    To be implemented
    '''
    pass

@app.route("/add-routine")
def add_routine():
    '''
    To be implemented
    '''
    pass

@app.route("/results")
def make_prediction():
    '''
    To be implemented
    '''
    # 1. get stations near points in routine

    # 2. retrieve data from API and format data to fit into model
    current_date= date.today()
    input_time_start = ###
    input_time_end = ###
    
 
    # 3. use model to generate predictions
    xgboost_model = xgb.XGBRegressor()
    xgboost_model.load_model("xgboost_model.json")
    predicted_values = xgboost_model.predict(formatted_data) # replace with variable name of formatted data from (2)
    stations = [] # replace with list of stations
    predicted_data = pd.DataFrame(list(zip(stations, predicted_values)), columns=["stations", "predicted_values"])

    # 4. generate probabilities
    # points_of_interest = [] # get points from routine
    result = get_rain_probability(predicted_data, points_of_interest)

    return result

