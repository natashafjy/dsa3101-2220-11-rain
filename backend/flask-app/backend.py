from flask import Flask, jsonify, request
import mysql.connector
import xgboost as xgb
from get_routine_rain_probability import *
from get_island_rain_probability import *
from get_last_rain import *
from get_data_from_api import *
from get_next_30_min_pred import *


app = Flask(__name__)

debug_mode = True

def cprint(val):
    if debug_mode:
        print(val,flush=True)


@app.route("/api/login", methods=["GET"])
def login():
    '''
    To be implemented
    '''
    # POST Request
    exist_in_db = True
    password_match = False

    exist_user_query = """
        SELECT *
        FROM USERS
        WHERE username = %s
     """
    # Assumes data comes in as a get request in the arguments
    username, password_input = request.args.get('username'), request.args.get('password')
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


@app.route("/api/signup", methods=["POST"])
def sign_up():
    '''
    To be implemented
    '''
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
    #access the username
    username = request.form["user_name"]
    #get all routines
    latest_routine_query = """
        SELECT R1.start_address, R1.end_address, R1.start_time, R1.end_time, R1.days_of_week
        FROM ROUTINES R1
        WHERE R1.username = %s;
        """
    db = mysql.connector.connect(host="db", user="root", password="examplePW",database="rainfall")
    cursor = db.cursor()

    #check number of routines user has
    cursor.execute(latest_routine_query, (username,) )
    routine_keys = ["start_point", "end_point", "start_time_value", "end_time_value", "days_of_week "]
    all_routines = cursor.fetchall()
    all_routines = {f'routine{indx}': dict(zip(routine_keys,val)) for indx,val in enumerate(all_routines, start=1)}
    response = {"has_routes": len(all_routines), 
                "routine": all_routines}
    return jsonify(response)


@app.route("/add_routine", methods=["POST"])
def add_routine():
    '''
    To be implemented
    '''
    latest_routine_query = """
    SELECT COUNT(*)
    FROM ROUTINES R1
    WHERE R1.username = %s
    """
    
    insert_routine_query = """
    INSERT INTO ROUTINES VALUES (%(user_name)s, %(routine_id)s, %(start_address)s, 
                                 %(start_long)s, %(start_lat)s, %(end_address)s, 
                                 %(end_long)s ,%(end_lat)s, %(start_time)s, 
                                 %(end_time)s, %(days_of_week)s)
    """
    #establish connection
    username = request.form["user_name"]
    req_data = dict(request.form)

    db = mysql.connector.connect(host="db", user="root", password="examplePW",database="rainfall")
    cursor = db.cursor()

    #get latest routine_id
    cursor.execute(latest_routine_query, (username,) )
    next_count = cursor.fetchone()[0] + 1
    req_data["routine_id"] = next_count

    cursor.execute(insert_routine_query, params=req_data )
    db.commit()

    cursor.close()
    db.close()
    return "Added_routine"

@app.route("/results")
def make_prediction():

    # 1. retrieve data from API and format data to fit into model
    curr_date, curr_time = get_curr_date_time()
    formatted_data = get_updated_data()
    formatted_data_pivot = get_updated_data_pivot()
 
    # 2. use model to generate predictions
    xgboost_model = xgb.XGBRegressor()
    xgboost_model.load_model("xgboost_model.json")
    predicted_data = get_next_30_min_pred(curr_date, curr_time, formatted_data, formatted_data_pivot, xgboost_model)

    # 3. generate probabilities
    # Assumes GET request has data = {"user_name": username, "routine_id": id}
    username, routine_id = request.form["user_name"], request.form["routine_id"]
    
    routine_info_query = """
        SELECT R1.start_long, R1.start_lat, R1.end_long, R1.end_lat
        FROM ROUTINES R1
        WHERE R1.username = %s
        AND R1.routine_id = %s
    """
    db = mysql.connector.connect(host="db", user="root", password="examplePW",database="rainfall")
    cursor = db.cursor()
    cursor.execute(routine_info_query, (username, routine_id) )
    points_of_interest = cursor.fetchone()[0]
    points_of_interest = tuple(map(lambda x: float(x),points_of_interest))
    points_of_interest = [points_of_interest[:2], points_of_interest[2:]]
    cursor.close()
    db.close()

    start_pred_df, last_pred_df = get_routine_rain_probability(predicted_data, points_of_interest)
    island_pred_df = get_island_rain_probability(predicted_data)

    # 4. find most recent instance of rain at the start point and end point of user's routine
    last_rain_start, last_rain_end = get_last_rain(points_of_interest)
    
    # convert to json 
    start_pred = start_pred_df.to_json()
    last_pred = last_pred_df.to_json()
    island_pred = island_pred_df.to_json()

    response = dict()
    response["start_pred"] = start_pred
    response["last_pred"] = last_pred
    response["island_pred"] = island_pred
    response["last_rain_start"] = last_rain_start
    response["last_rain_end"] = last_rain_end

    return jsonify(response)

