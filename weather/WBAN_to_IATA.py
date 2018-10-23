import pandas as pd
from datetime import datetime


time1 = datetime.now()
df = pd.read_csv('flight_data.csv')
time2 = datetime.now()
print('Time cost: ', time2-time1)
wban_faa = pd.read_csv('../Weather Data/emshr_lite.csv')
airports = pd.read_csv('../Weather Data/airport_download.txt',
                       sep='\t', index_col=0)
weather = pd.read_csv('../Weather Data/data/weather_pre.csv')
weather['WBAN'] = weather['STATION'].apply(lambda x: int(x[5:]))
airports = airports.merge(
    wban_faa, left_on='airports', right_on='FAA', how='inner'
).drop(columns= ['airports', 'state'])
new_airports = airports.reset_index(drop=True)
for i in range(new_airports.shape[0]):
    if weather[weather['WBAN'] == new_airports.loc[i, 'WBAN']].shape[0] == 0:
        new_airports = new_airports.drop([i])
new_airports = new_airports.rename(columns={'FAA':'IATA'})
new_airports.to_csv('../Weather Data/emshr_lite.csv', index=False)
