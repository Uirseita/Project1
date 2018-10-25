import pandas as pd

wban_iata = pd.read_csv('../Weather Data/wban_to_iata.csv')
weather = pd.read_csv('../Weather Data/data/weather_pre.csv')
weather['WBAN'] = weather['STATION'].apply(lambda x: int(x[5:]))
stations_df = weather.groupby('WBAN').first().loc[
              :, ['LATITUDE', 'LONGITUDE']
              ].reset_index()
stations_df = stations_df.merge(wban_iata, on='WBAN', how='inner')
airport_state = pd.read_csv('../Weather Data/airport_download.txt', sep='\t')
airport_state = airport_state.iloc[:, 1:].rename(columns={'airports': 'IATA'})
new_stations_df = stations_df.merge(
    airport_state, on='IATA', how='left'
).rename(columns={'state': 'STATE'})
new_stations_df = new_stations_df.sort_values(by='IATA')
new_stations_df.to_csv('./airport_location.csv', index=False)
