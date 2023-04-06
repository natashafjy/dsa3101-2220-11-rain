import pandas as pd
import numpy as np
import pykrige
import scipy

station_data = pd.read_csv("../data/station_data.csv", index_col = 0, dtype = {"device_id":"string", "name":"string", "latitude":"float64", "longitude":"float64"})

def get_rain_probability(predicted_data, points_of_interest):
    """
    input: 
        predicted data: dataframe containing the stations and their rainfall values (mm) at a specified time
        points_of_interest: (longitude, latitude) pairs of the points on the user's running route
    output:
        dataframe of possible rainfall values and their associated probabilities
    """

    data = predicted_data.merge(station_data, left_on="station", right_on="device_id")

    x = np.array(data["longitude"])
    y = np.array(data["latitude"])
    z = np.array(data["value"])
    
    ordinary_kriging = pykrige.OrdinaryKriging(x, y, z)

    point_pred_lst = []

    for point in points_of_interest:

        point_lat, point_long = point[0], point[1]

        # form grid of values around point
        gridx = np.arange(point_long-0.005, point_long+0.005, 0.001, dtype = "float64")
        gridy = np.arange(point_lat-0.005, point_lat+0.005, 0.001, dtype = "float64")

        # obtain predicted values and their variances using kriging
        zstar, ss = ordinary_kriging.execute("grid", gridx, gridy)

        zstar_clipped = zstar.clip(0) # replace negative values with 0 

        # convert 2d array to 1d
        zstar_1d = zstar_clipped.ravel()
        ss_1d = ss.ravel()

        # create dataframe of precipitation values and their variances for every coordinate in grid around point
        rain_probability_df = pd.DataFrame(list(zip(zstar_1d, ss_1d)), columns=["rain", "variance"])

        # drop rows where variance is negative/0 (prevent divide by 0 error)
        rain_probability_df = rain_probability_df[rain_probability_df["variance"] > 0]

        # calculate standard deviation, and calculate probability using CDF
        rain_probability_df["sd"] = np.sqrt(rain_probability_df["variance"])
        rain_probability_df["P=0"] = scipy.stats.norm(loc=rain_probability_df["rain"], scale=rain_probability_df["sd"]).cdf(0)
        rain_probability_df["rain_rounded"] = round(rain_probability_df["rain"],1)
        rain_probability_df["P=rain_rounded"] = scipy.stats.norm(loc=rain_probability_df["rain"], scale=rain_probability_df["sd"]).cdf(rain_probability_df["rain_rounded"])

        # add precipitation values and their associated probabilities to df
        point_pred_lst.append([point_long, point_lat, rain_probability_df["rain_rounded"].mean(), rain_probability_df["P=rain_rounded"].mean()])
        point_pred_lst.append([point_long, point_lat, 0, rain_probability_df["P=0"].mean()])

    # convert list of lists into dataframe
    point_pred_df = pd.DataFrame(point_pred_lst, columns=["longitude", "latitude", "precipiation", "probability"])

    return point_pred_df


def print_example():
    sample_data = pd.DataFrame({"station" : ["S71", "S92", "S203", "S230", "S223", "S226"],
                           "value" : [0.5, 0.7, 0.8, 1.4, 0.2, 0.2]})
    print(get_rain_probability(sample_data, [(1.29230, 103.78150), (1.28410, 103.78860), (1.29164, 103.77020), (1.30167, 103.76444), (1.29984, 103.80264), (1.27472, 103.80389)]))

# print_example()

    