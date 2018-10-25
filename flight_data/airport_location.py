import pandas as pd

wban_iata = pd.read_csv('../Weather Data/wban_to_iata.csv')
weather = pd.read_csv('../Weather Data/data/weather_pre.csv')
weather['WBAN'] = weather['STATION'].apply(lambda x: int(x[5:]))
stations_df = weather.groupby('WBAN').first().loc[
              :, ['LATITUDE', 'LONGITUDE']
              ].reset_index()
stations_df = stations_df.merge(wban_iata, on='WBAN', how='inner')
stations_df.to_csv('./airport_location.csv', index=False)
