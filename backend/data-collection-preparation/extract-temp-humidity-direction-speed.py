import pandas as pd
import requests
from functools import reduce


rainy_days = pd.read_csv("rainy_days_15mm.csv")

def spread_col(row_data):
    """
    Args:
        raw_data: string of list containing {"station_id" : XX, "value" : YY} dictionaries 

    Returns: 
        new dictionary {"XX1" : "YY1", ..., "XXN" : "YYN"}
    """
    row_data_lst = list(eval(row_data))
    new_dict = dict()
    for ddict in row_data_lst:
        if "value" in ddict.keys():
            new_dict[ddict["station_id"]] = ddict["value"]
        else:
            new_dict[ddict["station_id"]] = None
    return new_dict  


def extract_air_temperature_data(save_data = True):
    """"
    Args:
        save_data (default value = True): if True, data will be saved in a csv file
    
    Returns:
        dataframe of extracted air temperature data
    """

    url = "https://api.data.gov.sg/v1/environment/air-temperature"

    temp_df = []

    def extract_temp():
        for index, row in rainy_days.iterrows():
            date = f'{row["Year"]}-{row["Month"]:02}-{row["Day"]:02}'
            params = {"date": date} # YYYY-MM-DD
            data_dict = requests.get(url, params=params).json()
            readings_lst = data_dict["items"]
            readings_df = pd.DataFrame.from_dict(readings_lst)
            temp_df.append(readings_df)
        
    extract_temp()
    temp_data = pd.concat(temp_df, ignore_index=True)

    temp_data["loc_val"] = temp_data["readings"].map(lambda entry: spread_col(entry))

    temp_data_spread = temp_data.join(pd.json_normalize(temp_data["loc_val"]))

    if save_data is True:
        temp_data_spread.to_csv("temperature_data.csv")

    return temp_data_spread


def extract_humidity_data(save_data = True):
    """"
    Args:
        save_data (default value = True): if True, data will be saved in a csv file
    
    Returns:
        dataframe of extracted humidity data
    """

    url2 = "https://api.data.gov.sg/v1/environment/relative-humidity"

    humidity_df = []

    def extract_humidity():
        for index, row in rainy_days.iterrows():
            date = f'{row["Year"]}-{row["Month"]:02}-{row["Day"]:02}'
            params = {"date": date} # YYYY-MM-DD
            data_dict = requests.get(url2, params=params).json()
            readings_lst = data_dict["items"]
            readings_df = pd.DataFrame.from_dict(readings_lst)
            humidity_df.append(readings_df)
        
    extract_humidity()
    humidity_data = pd.concat(humidity_df, ignore_index=True)

    humidity_data["loc_val"] = humidity_data["readings"].map(lambda entry: spread_col(entry))

    humidity_data_spread = humidity_data.join(pd.json_normalize(humidity_data["loc_val"]))

    if save_data is True:
        humidity_data_spread.to_csv("humidity_data.csv")

    return humidity_data_spread


def extract_raw_wind_direction(save_model = True):
    """"
    Args:
        save_data (default value = True): if True, data will be saved in a csv file
    
    Returns:
        dataframe of raw wind direction data (columns are not spread)
    """

    url3 = "https://api.data.gov.sg/v1/environment/wind-direction"

    wind_dir_df = []

    def extract_wind_dir():
        for index, row in rainy_days.iterrows():
            date = f'{row["Year"]}-{row["Month"]:02}-{row["Day"]:02}'
            params = {"date": date} # YYYY-MM-DD
            data_dict = requests.get(url3, params=params).json()
            readings_lst = data_dict["items"]
            readings_df = pd.DataFrame.from_dict(readings_lst)
            wind_dir_df.append(readings_df)
        
    extract_wind_dir()

    wind_dir_data = pd.concat(wind_dir_df, ignore_index=True)

    if save_model is True:
        wind_dir_data.to_csv("wind_dir_data_raw.csv")

    return wind_dir_data



def extract_raw_wind_speed(save_data = True):
    """"
    Args:
        save_data (default value = True): if True, data will be saved in a csv file
    
    Returns:
        dataframe of raw wind speed data (columns are not spread)
    """

    url4 = "https://api.data.gov.sg/v1/environment/wind-speed"

    wind_spd_df = []

    def extract_wind_spd():
        for index, row in rainy_days.iterrows():
            date = f'{row["Year"]}-{row["Month"]:02}-{row["Day"]:02}'
            params = {"date": date} # YYYY-MM-DD
            data_dict = requests.get(url4, params=params).json()
            readings_lst = data_dict["items"]
            readings_df = pd.DataFrame.from_dict(readings_lst)
            wind_spd_df.append(readings_df)
        
    extract_wind_spd()
    wind_spd_data = pd.concat(wind_spd_df, ignore_index=True)

    if save_data is True:
        wind_spd_data.to_csv("wind_spd_data_raw.csv")

    return wind_spd_data


def extract_and_combine_data(save_data=True):
    """
    Args:
        save_data (default_value = True): saves data in a csv file
    Returns:
        dataframe with columns: "date", "time", "station", "value", "humidity", "temperature",	"wind_direction", "wind_speed"
    """
    

    def melt_df(df, col_name):

        df1 = df.drop(columns = ["readings", "loc_val"])
        df1[['date_time', 'timezone']] = df1['timestamp'].str.split('+', expand = True)
        df1[['date', 'time']] = df1['date_time'].str.split('T', expand = True)
        df1 = df1.drop(columns = ["timestamp", "date_time", "timezone"])

        df1[['hh', 'mm', 'ss']] = df1["time"].str.split(":", expand = True)

        df1["mm"] = df1["mm"].astype(int)
        df1_valid_timings = df1[df1["mm"] % 5 == 0]
        df1_valid_timings = df1_valid_timings.drop(columns = ["hh", "mm", "ss"])

        melted_df = df1_valid_timings.melt(id_vars = ["date", "time"], var_name = "station", value_name = col_name)

        return melted_df


    temp_data = extract_air_temperature_data(False)
    humid_data = extract_humidity_data(False)

    melted_temp_data = melt_df(temp_data, "temperature")
    melted_humid_data = melt_df(humid_data, "humidity")

    
    def melt_raw_df(df, col_name):
        df[['date_time', 'timezone']] = df['timestamp'].str.split('+', expand = True)
        df[['date', 'time']] = df['date_time'].str.split('T', expand = True)
        df = df.drop(columns = ["timestamp", "date_time", "timezone"])

        df[['hh', 'mm', 'ss']] = df["time"].str.split(":", expand = True)
        df["mm"] = df["mm"].astype(int)

        df_valid_timings = df[df["mm"] % 5 == 0]
        df_valid_timings = df_valid_timings.drop(columns = ["hh", "mm", "ss"])

        df["loc_val"] = df["readings"].map(lambda entry: spread_col(entry))

        df = df.drop(columns = ["readings"])
        data = df.join(pd.json_normalize(df["loc_val"]))
        data = data.drop(columns = ["loc_val"])
        melted_df = data.melt(id_vars = ["date", "time"], var_name = "station", value_name = col_name)
        
        return melted_df

    raw_wind_dir_data = extract_raw_wind_direction(False)
    raw_wind_spd_data = extract_raw_wind_speed(False)

    melted_wind_dir_data = melt_raw_df(raw_wind_dir_data, "wind_direction")    
    melted_wind_spd_data = melt_raw_df(raw_wind_spd_data, "wind_speed")

    rain_data = pd.read_csv("rain_data_full.csv")

    # combines data
    all_data = reduce(lambda x,y: pd.merge(x, y, on = ["date", "time", "station"], how = "outer"), [rain_data, melted_humid_data, melted_temp_data, melted_wind_dir_data, melted_wind_spd_data])
    
    all_data = all_data[["date", "time", "station", "value", "humidity", "temperature",	"wind_direction", "wind_speed"]]

    if save_data is True:
        all_data.to_csv("all_data.csv")

    return all_data


if __name__ == "__main__":
    extract_and_combine_data()