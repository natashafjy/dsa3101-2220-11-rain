
import pandas as pd

def clean_weather_data(save_final_csv = True):
    """
    Cleans data extracted from weather.gov

    Args:
        save_final_csv (default value = True): boolean value that determines if final dataframe is into a csv named "rainy_days_15mm.csv"
    
    Returns:
        pandas dataframe containing the columns: "Year", "Month", "Day" where daily rainfall total >= 15 mm.
    """

    weather_data = pd.read_csv("weather_data.csv")

    # convert "Daily Rainfall Total (mm)" column to numeric
    weather_data["Daily Rainfall Total (mm)"] = pd.to_numeric(weather_data["Daily Rainfall Total (mm)"], errors="coerce")

    # remove rows where "Daily Rainfall Total (mm)" < 15mm
    no_rain_idx = weather_data[ (weather_data["Daily Rainfall Total (mm)"] < 15) ].index
    weather_data.drop(no_rain_idx, inplace=True)
    weather_data.reset_index(drop = True, inplace = True)

    # convert remaining columns to numeric
    numeric_cols = ["Highest  30-min Rainfall (mm)", "Highest  60-min Rainfall (mm)", "Highest 120-min Rainfall (mm)", "Mean Wind Speed (km/h)", "Mean Temperature (degree celsius)", "Maximum Temperature (degree celsius)", "Minimum Temperature (degree celsius)", "Mean Wind Speed (km/h)", "Max Wind Speed (km/h)"]

    for col in numeric_cols:
        weather_data[col] = pd.to_numeric(weather_data[col], errors="coerce")


    # split "Date" into "Day" and "Month" columns, then convert to numeric
    weather_data[["Day", "Month"]] = weather_data["Date"].str.split(' ', expand=True)
    weather_data["Day"] = pd.to_numeric(weather_data["Day"])
    weather_data['Month'] = pd.to_datetime(weather_data.Month, format='%b').dt.month

    # reorder columns for convenience
    reordered_cols = ['Location', 'Year', 'Date', 'Day', 'Month', 'Daily Rainfall Total (mm)',
                    'Highest  30-min Rainfall (mm)', 'Highest  60-min Rainfall (mm)', 'Highest 120-min Rainfall (mm)',
                    'Mean Temperature (degree celsius)', 'Maximum Temperature (degree celsius)', 'Minimum Temperature (degree celsius)',
                    'Mean Wind Speed (km/h)', 'Max Wind Speed (km/h)']
    weather_data = weather_data[reordered_cols]

    # extract and export dates to csv
    rainy_days = weather_data[["Year", "Month", "Day"]]
    rainy_days.drop_duplicates(inplace = True)

    if save_final_csv is True:
        rainy_days.to_csv("rainy_days_15mm.csv")

    return rainy_days

if __name__ == "__main__":
    clean_weather_data()