from flask import Flask
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

    # 3. use model to generate predictions
    # predicted_data = pd.DataFrame() # to edit

    # generate probabilities
    # points_of_interest = []] # get points from routine
    result = get_rain_probability(predicted_data, points_of_interest)

    return result

