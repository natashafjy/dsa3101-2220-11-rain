from flask import Flask


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
    pass

