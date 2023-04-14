import pandas as pd
import requests

def extract_all_stations(save_data = True):
    """
    Args:
        save_data (default value = True): whether station data should be saved in a file named "station_data.csv"
    
    Returns:
        a dataframe containing the columns "device_id", "name", "latitude", "longitude"  of all the weather stations (both active and inactive)
    
    """
    rainy_days = pd.read_csv("rainy_days_15mm.csv")
    url = "https://api.data.gov.sg/v1/environment/rainfall"

    all_stations_df = []

    def extract_stations():
        for index, row in rainy_days.iterrows():
            date = f'{row["Year"]}-{row["Month"]:02}-{row["Day"]:02}'
            params = {"date": date} # YYYY-MM-DD
            data_dict = requests.get(url, params=params).json()
            stations_lst = data_dict["metadata"]["stations"]
            stations_df = pd.DataFrame.from_dict(stations_lst)
            all_stations_df.append(stations_df)
            
    extract_stations()

    all_stations_data = pd.concat(all_stations_df, ignore_index=True)

    all_stations_data = all_stations_data.join(pd.json_normalize(all_stations_data["location"]))

    all_stations_data = all_stations_data[["device_id", "name", "latitude", "longitude"]]

    all_stations = all_stations_data.drop_duplicates(ignore_index = True)

    if save_data is True:
        all_stations.to_csv("station_data.csv")

    return all_stations

