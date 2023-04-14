import pandas as pd
import requests


def extract_rainfall_values_all(save_intermediate_data = True, save_final_data = True, drop_0_vals = False):
    """
    This function extracts rainfall values from the dates extracted by the weather-data.py code, which is stored in the rainy_days_15mm.csv file.

    ## WARNING: takes 75 minutes to extract 1131 days' worth of data

    Args:
        save_intermediate_data (default value = True): saves the raw data obtained from the data.gov.sg API into a csv file named "rain_values_15mm.csv"
        save_final_data (default value = True): saves the melted data without 0's or NaN's into a csv file named "rain_data.csv" if drop_0_vals is True, else save as "rain_data_all.csv"
        drop_0_vals (default value = False): if True, drop rows where rain value == 0mm or NaN, otherwise keep in data set

    Return:
        pandas dataframe with the following columns: "date", "time", "station", "value"

    """

    # 1. Accessing data from data.gov.sg website
    rainy_days = pd.read_csv("../data/rainy_days_15mm.csv")
    url = "https://api.data.gov.sg/v1/environment/rainfall"

    data_df = []

    def extract_data():
        for index, row in rainy_days.iterrows():
            date = f'{row["Year"]}-{row["Month"]:02}-{row["Day"]:02}'
            params = {"date": date} # YYYY-MM-DD
            data_dict = requests.get(url, params=params).json()
            readings_lst = data_dict["items"]
            readings_df = pd.DataFrame.from_dict(readings_lst)
            data_df.append(readings_df)
        
    data = pd.concat(data_df, ignore_index=True)
    
    extract_data()
    
    # export extracted data
    if save_intermediate_data is True:
        data.to_csv("../data/rain_values_15mm.csv")

    # 2. Convert the 'readings' column into a more useful format

    # convert readings col from a list of dicts containing the keys "station_id" and "value" to a dict of station_id-value key-value pairs
    def spread_column(lst):
        new_dict = dict()
        for ddict in lst:
            new_dict[ddict["station_id"]] = ddict["value"]
        return new_dict

    data["loc_val"] = data["readings"].map(lambda entry: spread_column(entry))

    data = data.join(pd.json_normalize(data["loc_val"]))

    # 3. Tidy up data

    # drop redundant columns
    new_df = data.drop(columns = ["readings", "loc_val"])

    # reshape dataframe
    melted_df = new_df.melt(id_vars = ["timestamp"], var_name = "station")

    if drop_0_vals:
        # remove NaNs and 0's from "values" column
        final_df = melted_df.dropna()
        no_rain_idx = final_df[ (final_df["value"] == 0)].index
        final_df.drop(no_rain_idx, inplace=True)
    
    final_df.reset_index(drop = True, inplace = True)

    # split timestamp column into 3 cols
    final_df[['date_time', 'timezone']] = final_df['timestamp'].str.split('+', expand=True)
    final_df[['date', 'time']] = final_df['date_time'].str.split('T', expand=True)

    # extract necessary columns
    final_df = final_df[["date", "time", "station", "value"]]
    
    # export data
    if save_final_data is True:
        if drop_0_vals:
            final_df.to_csv("../data/rain_data.csv")
        else:
            final_df.to_csv("../data/rain_data_all.csv")

    return final_df


if __name__ == "__main__":
    extract_rainfall_values_all()