# ShortVIX
Group members: Sean Abreau, Matthew Owen, Nakarit Suthapreda, Qingyu Ye

How to recreate dataset:
1) go to bts website and download "Reporting Carrier On-Time Performance (1987-present)" filter to only the years 2016 & 2017
  https://www.transtats.bts.gov/Tables.asp?DB_ID=120
2) go to noaa website and produce 65 data requests for all 324 airports WBAN stations (will take multiple days) can find WBAN to FAA airport code in our "wban_to_iata" file
   https://www.ncdc.noaa.gov/cdo-web/datatools/lcd
3) use our file "tail_num_with_number_of_seats" to map tail numbers to seat counts and merge

In all honesty replicating our data is not feasible and should you want our data please reach out to us

Introduction to some .py scripts:

./aa_tail_num_matching.py
Match American Airlines nose numbers into tail numbers

./tail_num_data_scraping.py
Scrape tail numbers data from FAA.gov

./update_tail_num_result.py
Functions that can update information manually to the tail number data

./flight_data/airport_location.py
Merge location data to the airport IATA code

./flight_data/plot_on_us_map.py
Make visualizations on US map, see also ./visualizations/Qingyu_Visualization.ipynb

./weather/WBAN_to_IATA.py
Match WBAN number to IATA code

./weather/average_delay_minutes_of_different_weather_types.py
Calculate average delay minutes of different weather types for plots, see also ./visualizations/Qingyu_Visualization.ipynb

./weather/matched_weather_of_flights.py
Find the matched weather information in weather dataframe

./weather/matched_weather_of_flights_global_variances.py
Find the matched weather information in weather dataframe, using global variances, slightly faster than matched_weather_of_flights.py
