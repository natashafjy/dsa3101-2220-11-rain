from flask import Flask, jsonify, request
import mysql.connector
import xgboost as xgb
from get_rain_probability import *

app = Flask(__name__)

debug_mode = True

def cprint(val):
    if debug_mode:
        print(val,flush=True)


@app.route("/", methods=["GET", "POST"])
def login():
    '''
    To be implemented
    '''
    if request.method == "GET":
        return "Hiii im on the login page"

    # POST Request
    exist_in_db = True
    password_match = False

    exist_user_query = """
        SELECT *
        FROM USERS
        WHERE username = %s
     """
    # Assumes data comes in as a form-data
    cprint(f'req.form = {request.form}')   
    username, password_input = request.form["user_name"], request.form["password"]
    db = mysql.connector.connect(host="db", user="root", password="examplePW",database="rainfall")
    cursor = db.cursor()
    cursor.execute(exist_user_query, (username,))
    all_rows = cursor.fetchall()
    if len(all_rows) == 0:
        exist_in_db = False

    #assumes unique (username)
    password_set = set(map(lambda x: x[-1], all_rows))
    cprint(f'password_set is {password_set}')
    if password_input in password_set:
        password_match = True
    
    cursor.close()
    db.close()
    response = {"exist":exist_in_db, "match": password_match}
    return jsonify(response)

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    '''
    To be implemented
    '''
    if request.method == "GET":
        return "Hii im trying to signup"
    
    #else POST
    exist_in_db = True
    added_to_db = False

    # Assumes data comes in as a form-data
    cprint(f'req.form = {request.form}')   
    username, password = request.form["user_name"], request.form["password"]

    exist_user_query = """
        SELECT *
        FROM USERS
        WHERE username = %s
    """

    add_user_query = "INSERT INTO USERS(username,password) VALUES (%s, %s)"

    #establish connection
    db = mysql.connector.connect(host="db", user="root", password="examplePW",database="rainfall")
    cursor = db.cursor()

    #check if user in db
    cursor.execute(exist_user_query, (username,) )
    rows = cursor.fetchall()

    #assumes unique (username)
    password_set = set(map(lambda x: x[-1], rows))
    cprint(f'password_set is {password_set}')

    #add users if user_name not taken
    if len(rows) == 0 :
        exist_in_db = False
        cursor.execute(add_user_query, (username, password) )
        db.commit()
        added_to_db = True

    cursor.close()
    db.close()
    response = {"exist": exist_in_db, "success": added_to_db}
    return jsonify(response)

@app.route("/gallery", methods = ["GET"])
def gallery():
    """
    To be implemented
    """
    if request.method == "GET":
        #access the username
        #get all routines
        
    return "Not implemented yet"


@app.route("/add-routine", methods=["GET", "POST"])
def add_routine():
    '''
    To be implemented
    '''
    return "Add_routine"

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

