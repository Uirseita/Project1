# ShortVIX
Group members: Sean Abreau, Matthew Owen, Nakarit Suthapreda, Qingyu Ye

How to recreate dataset:
1) go to bts website and download "Reporting Carrier On-Time Performance (1987-present)" filter to only the years 2016 & 2017
  https://www.transtats.bts.gov/Tables.asp?DB_ID=120
2) go to noaa website and produce 65 data requests for all 324 airports WBAN stations (will take multiple days) can find WBAN to FAA airport code in our "wban_to_iata" file
   https://www.ncdc.noaa.gov/cdo-web/datatools/lcd
3) use our file "tail_num_with_number_of_seats" to map tail numbers to seat counts and merge

In all honesty replicating our data is not feasible and should you want our data please reach out to us
