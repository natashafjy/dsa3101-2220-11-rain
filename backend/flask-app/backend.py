from flask import Flask, jsonify, request
import mysql.connector
import xgboost as xgb
from get_routine_rain_probability import *
from get_last_rain import *
from get_data_from_api import *
from get_next_30_min_pred import *


app = Flask(__name__)

###### Helper functions ######
debug_mode = True

def cprint(val):
    if debug_mode:
        print(val,flush=True)

def establish_db_connection():
    return mysql.connector.connect(host="db", 
                                   user="root",
                                   password="examplePW",
                                   database="rainfall")

def get_user_password(connection, username):
    exist_user_query = """
        SELECT *
        FROM USERS
        WHERE username = %s
     """
    cursor = connection.cursor()
    cursor.execute(exist_user_query, (username,))
    user_and_password = cursor.fetchall()
    cursor.close()
    return user_and_password

def add_user_to_db(connection, username, password):
    cursor = connection.cursor()
    add_user_query = "INSERT INTO USERS(username,password) VALUES (%s, %s)"
    cursor.execute(add_user_query, (username, password) )
    connection.commit()
    cursor.close()

def get_user_routines(connection, username):
    all_user_routine_query = """
        SELECT R1.start_address, R1.end_address, R1.start_time, R1.end_time, R1.days_of_week
        FROM ROUTINES R1
        WHERE R1.username = %s;
        """
    cursor = connection.cursor()
    #check number of routines user has
    cursor.execute(all_user_routine_query, (username,) )
    all_routines = cursor.fetchall()
    cursor.close()
    return all_routines

def add_user_routine(connection, params):
    insert_routine_query = """
    INSERT INTO ROUTINES VALUES (%(user_name)s, %(routine_num)s, %(start_address)s, 
                                 %(start_long)s, %(start_lat)s, %(end_address)s, 
                                 %(end_long)s ,%(end_lat)s, %(start_time)s, 
                                 %(end_time)s, %(days_of_week)s)
    """
    cursor = connection.cursor()
    cursor.execute(insert_routine_query, params)
    connection.commit()
    cursor.close()

def get_specific_routine(connection, username, routine_id):
    routine_info_query = """
        SELECT R1.start_long, R1.start_lat, R1.end_long, R1.end_lat
        FROM ROUTINES R1
        WHERE R1.username = %s
        AND R1.routine_id = %s
    """
    cursor = connection.cursor()
    cursor.execute(routine_info_query, (username, routine_id) )
    routine_info = cursor.fetchone()
    cursor.close()
    return routine_info

###### End of Helper functions ######


@app.route("/api/login", methods=["GET"])
def login():
    exist_in_db = True
    password_match = False

    # Assumes data comes in as a get request in the arguments
    username, password_input = request.args.get('username'), request.args.get('password')
    db = establish_db_connection()
    all_rows = get_user_password(db, username)
    if len(all_rows) == 0:
        exist_in_db = False

    #assumes unique (username)
    password_set = set(map(lambda x: x[-1], all_rows))
    cprint(f'password_set is {password_set}')
    if password_input in password_set:
        password_match = True

    response = {"exist":exist_in_db, "match": password_match}
    return jsonify(response)


@app.route("/api/signup", methods=["POST"])
def sign_up():
    exist_in_db = True
    username, password = request.args.get("username"), request.args.get("password")
    
    #establish connection
    db = establish_db_connection()
    #check if user in db
    rows = get_user_password(db, username)

    #add users if user_name not taken
    if len(rows) == 0 :
        exist_in_db = False
        add_user_to_db(db,username,password)

    db.close()
    response = {"exist": exist_in_db}
    return jsonify(response)

@app.route("/api/gallery", methods = ["GET"])
def gallery():
    #access the username
    username = request.args.get("username")
    routine_keys = ["start_point", "end_point", "start_time_value", "end_time_value", "days_of_week"]
    #get all routines
    db = establish_db_connection()
    all_routines = get_user_routines(db, username)
    all_routines = {f'routine{indx}': dict(zip(routine_keys,val)) for indx,val in enumerate(all_routines, start=1)}
    response = {"routine_num": len(all_routines), 
                "routine": all_routines}
    return jsonify(response)


@app.route("/api/add_routine", methods=["POST"])
def add_routine():   
    username = request.args.get("username")
    req_data = { "user_name":username, "start_address":request.args.get("start_address"), 
                 "start_long":request.args.get("start_long"),"start_lat":request.args.get("start_lat"),
                  "end_address":request.args.get("end_address"), "end_long":request.args.get("end_long"),
                  "end_lat":request.args.get("end_lat"), "start_time":request.args.get("start_time"),
                  "end_time":request.args.get("end_time"), "days_of_week":request.args.get("days_of_week"),                
                }

    db = establish_db_connection()

    #get next routine_id
    next_count = len(get_user_routines(db, username)) + 1
    req_data["routine_num"] = next_count
    add_user_routine(db, req_data)
    db.close()
    return "Added_routine"

@app.route("/api/results", methods=["GET"])
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
    username, routine_id = request.args.get("username"), request.args.get("routine_num")

    db = establish_db_connection()
    points_of_interest = get_specific_routine(db, username, routine_id)
    points_of_interest = tuple(map(lambda x: float(x),points_of_interest))
    points_of_interest = [points_of_interest[:2], points_of_interest[2:]]
    db.close()

    start_pred_df, last_pred_df = get_routine_rain_probability(predicted_data, points_of_interest)

    island_pred_df = predicted_data.merge(station_data, left_on="station", right_on="device_id")
    island_pred_df = island_pred_df[["longitude", "latitude", "time", "value"]]
    island_pred_df["predicted_rain"] = island_pred_df["value"]
    island_pred_df["P(predicted_rain > 0)"] = 0.7 # remove when frontend graph is updated


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
