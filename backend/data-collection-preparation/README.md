This folder contains code for collecting data and preparing the data to be used in model training.

The following table summarises the recommended flow of script execution and their corresponding outputs:

| script | purpose | output file | note | 
|--|--|--|--|
| weather_scraper.py | obtains historical daily rainfall values | weather_data.csv | |
| clean-weather-data-csv.py | cleans data and find days where daily rainfall >= 15mm | rainy_days_15mm.csv | |
| extract-rainfall-values-all.py | obtains rainfall data from data.gov.sg | rain_data.csv or rain_data_all.csv | different csvs generated depending on whether rows with 0/NaN's are kept |
| extract-temp-humidity-direction-speed.py | extracts additional environment data from data.gov.sg | all_data.csv | not included in model training |
| extract-stations.py | extract locations of all weather stations | station_data.csv | | 
| preprocess-data.py | reshape data into format to be used in model training | sliding_window_data.csv | |