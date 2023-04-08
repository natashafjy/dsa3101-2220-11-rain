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
    
    def get_time_tuples(date_time_tuple):
    	date_str, time_str = date_time_tuple
   	datetime_obj = datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M:%S')
    	result = []
    	for i in range(7,13):
        		new_datetime_obj = datetime_obj - timedelta(minutes=i*5)
        		new_date_str = new_datetime_obj.strftime('%Y-%m-%d')
        		new_time_str = new_datetime_obj.strftime('%H:%M:%S')
        		result.append((new_date_str, new_time_str))
    	return result
    
    url = "https://api.data.gov.sg/v1/environment/rainfall"
    
    start_timestamp_extracted = get_time_tuples((current_date, input_time_start))
    end_timestamp_extracted = get_time_tuples((current_date, input_time_end))
    
    def extract_data():
    	for row in start_timestamp_extracted:
        		params = {"date": row[0]} # YYYY-MM-DD
        		data_dict = requests.get(url, params=params).json()
        		readings_lst = data_dict["items"]
        		readings_df = pd.DataFrame.from_dict(readings_lst)
       		data_df.append(readings_df)
        
    data = pd.concat(data_df, ignore_index=True)
    
    def spread_column(lst):
    	new_dict = dict()
    	for ddict in lst:
        		new_dict[ddict["station_id"]] = ddict["value"]
   	return new_dict

	data["loc_val"] = data["readings"].map(lambda entry: spread_column(entry))
	data = data.join(pd.json_normalize(data["loc_val"]))
	data = data.drop(columns = ["readings", "loc_val"])
	data = data.melt(id_vars = ["timestamp"], var_name = "station")
	
	final_df = data.dropna() #question ???
	no_rain_idx = final_df[ (final_df["value"] == 0)].index
	final_df.drop(no_rain_idx, inplace=True)
	final_df.reset_index(drop = True, inplace = True)
	
	final_df[['date_time', 'timezone']] = final_df['timestamp'].str.split('+', expand=True)
	final_df[['date', 'time']] = final_df['date_time'].str.split('T', expand=True)
	
	
	lst_of_rows = []
	for i in range(1,len(final_df)):
    		orig_date, orig_time, orig_stn, orig_val = rain_data.iloc[i,0], rain_data.iloc[i,1], rain_data.iloc[i,2], rain_data.iloc[i,3]
    	nearest_k_stns = k_nearest_dic[orig_stn]
    	newRow = [orig_date, orig_time, orig_stn, orig_val]
 
    	for time_indx,(date,time_stamp) in enumerate(get_time_tuples((orig_date, orig_time)),start=1):
        		for (stn,dist) in nearest_k_stns:
            		newRow.append(-5*time_indx-30)
            		newRow.append(stn)
            		newRow.append(dist)
            		newRow.append(rain_data_pivot.get((date,time_stamp),{}).get(stn,np.nan))
        			newRow.append(-5*time_indx-30)
        			newRow.append(orig_stn)
        			newRow.append(0)
        			newRow.append(rain_data_pivot.get((date,time_stamp),{}).get(orig_stn,np.nan))
    	lst_of_rows.append(newRow)
        
    #should change to json format but dataframe may be straightforward
 
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

