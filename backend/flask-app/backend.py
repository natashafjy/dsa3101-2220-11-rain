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
    """
    Establishes a connection with the mysql to the "rainfall" database
    Logs in using the root user and the password created in the 
    docker-compost.yml file

    Args:
        None  
    
    Returns:
        CMySQLConnection object, # connection for the database

    """
    return mysql.connector.connect(host="db", 
                                   user="root",
                                   password="examplePW",
                                   database="rainfall")

def get_user_password(connection, username):
    """
    Queries the database to get all rows with the same username as the 
    input "username"

    Args:
        connection (CMySQLConnection object) : database connection for us to create a cursor
        username (string) : username that user input
    Returns:
        user_and_password (List< Tuple<Str,Str> >) e.g [("user1","pw1"),] : List of Tuples with matching usernames as the username input
    """
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
    """
    Adds the user to the USERS table in the database,
    with the given username and password

    Args:
        connection (CMySQLConnection object) : database connection for us to create a cursor
        username (string) : username that user input
        password (string) : password that user input
    Returns:
        None
    """
    cursor = connection.cursor()
    add_user_query = "INSERT INTO USERS(username,password) VALUES (%s, %s)"
    cursor.execute(add_user_query, (username, password) )
    connection.commit()
    cursor.close()

def get_user_routines(connection, username):
    """
    Get all routines that a particular user has

    Args:
        connection (CMySQLConnection object) : database connection for us to create a cursor
        username (string) : username of user

    Returns:
        all_routines ( List< Tuple<Str,Str,Str,Str,Str> >) e.g [("NUS","NTU","10:10","13:10","Mon Tues"), ... ] : List of all routines a user has
    """
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
    """
    Adds the routine to the ROUTINES table in the database,
    with the given parameters

    Args:
        connection (CMySQLConnection object) : database connection for us to create a cursor
        params (Dict) : parameters for a routine

    Returns:
        None

    """
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
    """
    Get one specified routines for a particular user

    Args:
        connection (CMySQLConnection object) : database connection for us to create a cursor
        username (string) : username of user
        routine_id (int) : routine that the specified user
    Returns:
        routine_info (List< Tuple<Str,Str,Str,Str> >) e.g [("NUS","NTU","10:10","13:10","Mon Tues"), ... ] : List of all routines a user has
    """

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
    """
    This route handles the login page. It checks if the username exists in the database and 
    if the user exists, checks if the password matches with what's in the database

    Parameters:
        None
    
    Arguments to request URL:
        username : str
        password : str

    Returns:
        JSON response:
        {
            "exist": boolean, # Indicates whether the provided username exists in the database
            "match": boolean  # Indicates whether the provided password matches the one associated with the username
        }
    """
    exist_in_db = False
    password_match = False

    # Assumes data comes in as a get request in the arguments
    username, password_input = request.args.get('username'), request.args.get('password')
    db = establish_db_connection()
    all_rows = get_user_password(db, username)
    if len(all_rows) > 0:
        exist_in_db = True

    #assumes unique (username)
    password_set = set(map(lambda x: x[-1], all_rows))
    cprint(f'password_set is {password_set}')
    cprint((username,password_input))
    if exist_in_db and (password_input in password_set):
        password_match = True

    response = {"exist":exist_in_db, "match": password_match}
    return jsonify(response)


@app.route("/api/signup", methods=["POST"])
def sign_up():
    """
    This route handles the sign-up page. It checks whether the provided username already exists in the database.
    If the username doesn't exist, it adds the user to the database and returns a JSON response with the 'exist' key set to False; 
    otherwise, it returns a JSON response with the 'exist' key set to True.

    Parameters:
        None

    Arguments to request URL:
        username : str
        password : str

    Returns:
        JSON response:
        {
            "exist": boolean, # Indicates whether the provided username already exists in the database
        }
    """

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
    """
    This route handles the gallery page. It queries the database to get information on
    all the routines a user has and return the start_point, end_point, start_time, end_time
    and days_of_week for every routine.
    If user has no routines, "routine_num" will be 0 and "routine" will be an empty dictionary.

    Parameters:
        None

    Arguments to request URL:
        username : str

    Returns:
        JSON response:
        {
            "routine_num": int
            "routine" : { 
                routine1 : {
                    "start_point": "NUS",
                    "end_point": "NTU",
                    "start_time_value": "10:00",
                    "end_time_value": "13:00",
                    "days_of_week": "Mon Tue Wed"
                    },
                "routine2": {
                    "start_point": "NTU",
                    "end_point": "NUS",
                    "start_time_value": "08:10",
                    "end_time_value": "09:40",
                    "days_of_week": "Sat Sun"
                    }
                }
        }
    """
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
    """
    This route handles the add_routine page. It queries the database to get the number of 
    routines a user has and combines that with the provided information about a routine 
    and adds that into the database. Returns a string "Added_routine" when the record 
    is successfully added to the database. 
    

    Parameters:
        None

    Arguments to request URL:
        username : str
        start_address : str
        start_long : str
        start_lat : str
        end_address : str
        end_long : str
        end_lat : str
        start_time : str
        end_time : str
        days_of_week : str

    Returns:
        The string "Added_routine"

    """
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
    """
    This route handles the results page. It makes predictions for whether it will
    rain at 0 to 30 minutes from now, in 5 minute intervals. It will make API 
    calls to data.gov to access data for the previous 30 minutes and pass the 
    data into a saved xgboost model for prediction.

    Parameters:
        None

    Arguments to request URL:
        username : str
        routine_num : int

    Returns:
        JSON response:
        {
            "start_pred" :
                {
                    "longitude" : {"0": int, "1":int, "2":int, "3":int, "4":int, "5":int, "6":int},
                    "latitude" : {"0": int, "1":int, "2":int, "3":int, "4":int, "5":int, "6":int},
                    "time" : {"0": 0, "1": 5, "2": 10, "3": 15, "4": 20, "5": 25, "6": 30},
                    "predicted_rain" : {"0": float, "1":float, "2":float, "3":float, "4":float, "5":float, "6":float},
                    "P(predicted_rain > 0)" : float
                }
            "last_pred" :
                {
                    "longitude" : {"0": int, "1":int, "2":int, "3":int, "4":int, "5":int, "6":int},
                    "latitude" : {"0": int, "1":int, "2":int, "3":int, "4":int, "5":int, "6":int},
                    "time" : {"0": 0, "1": 5, "2": 10, "3": 15, "4": 20, "5": 25, "6": 30},
                    "predicted_rain" : {"0": float, "1":float, "2":float, "3":float, "4":float, "5":float, "6":float},
                    "P(predicted_rain > 0)" : float
                }
            "island_pred" : 
                {
                    "longitude" : 
                        { 
                            index (str) : value (float)
                            ... many rows
                        },
                    "latitude" : 
                        { 
                            index (str) : value (float)
                            ... many rows
                        },
                    "time" : 
                        {
                            index (str) : value (float)
                            ... many rows
                        },
                    "predicted_rain" :
                        {
                            index (str) : value (float)
                            ... many rows
                        },
                    "P(predicted_rain > 0)" : float
                }
            "last_rain_start" : int , # Indicates minutes since last instance of rain at the starting location
            "last_rain_end" : int , # Indicates minutes since last instance of rain at the starting location

        }

    """
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
