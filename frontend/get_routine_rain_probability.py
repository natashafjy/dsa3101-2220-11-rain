import pandas as pd
import numpy as np
import pykrige
import scipy

station_data = pd.read_csv("data/station_data.csv", index_col = 0, dtype = {"device_id":"string", "name":"string", "latitude":"float64", "longitude":"float64"})

def get_routine_rain_probability(predicted_data, points_of_interest):
    """
    input: 
        predicted data: dataframe containing the stations and their rainfall values (mm) at a specified time
        points_of_interest: (longitude, latitude) of the start and end points on the user's running route 
    output:
        dataframe of longitude, latitude, time, precipitation (mm), probability that rain = 0
    """

    data = predicted_data.merge(station_data, left_on="station", right_on="device_id")

    start_point_pred_lst = []
    end_point_pred_lst = []

    for time in range(0, 31, 5):
        data_at_time = data[data["time"] == time]
        x = np.array(data_at_time["longitude"])
        y = np.array(data_at_time["latitude"])
        z = np.array(data_at_time["value"])
    
        ordinary_kriging = pykrige.OrdinaryKriging(x, y, z, coordinates_type = "geographic", variogram_model = "gaussian")

        for point_num in range(len(points_of_interest)):

            point_long, point_lat = points_of_interest[point_num][0], points_of_interest[point_num][1]

            # form grid of values around point
            gridx = np.arange(point_long-0.0005, point_long+0.0005, 0.0001, dtype = "float64")
            gridy = np.arange(point_lat-0.0005, point_lat+0.0005, 0.0001, dtype = "float64")

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
            # rain_probability_df["predicted_rain"] = round(rain_probability_df["rain"], 1)
            # no need: rain_probability_df["P=rain_rounded"] = scipy.stats.norm(loc=rain_probability_df["rain"], scale=rain_probability_df["sd"]).cdf(rain_probability_df["rain_rounded"])

            # add precipitation values and their associated probabilities to df
            prob_of_rain = round(1 - rain_probability_df["P=0"].mean(), 3)

            if point_num == 0:
                start_point_pred_lst.append([point_long, point_lat, time, round(rain_probability_df["rain"].mean(), 1), prob_of_rain])
            else: 
                end_point_pred_lst.append([point_long, point_lat, time, round(rain_probability_df["rain"].mean(), 1), prob_of_rain])

    # convert list of lists into dataframe
    start_point_pred_df = pd.DataFrame(start_point_pred_lst, columns=["longitude", "latitude", "time", "predicted_rain", "P(predicted_rain > 0)"])
    end_point_pred_df = pd.DataFrame(end_point_pred_lst, columns=["longitude", "latitude", "time", "predicted_rain", "P(predicted_rain > 0)"])
    return start_point_pred_df, end_point_pred_df

