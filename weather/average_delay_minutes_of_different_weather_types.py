import numpy as np
import pandas as pd
import re


def find_closest_date(timepoint, time_series):
    # takes a pd.Timestamp() instance and a pd.Series with dates in it
    # calcs the delta between `timepoint` and each date in `time_series`
    # return the index of closest datetime
    timepoint = np.datetime64(timepoint)
    deltas = np.abs(np.subtract(time_series.values, timepoint))
    idx_closest_date = np.argmin(deltas)
    return time_series.index[idx_closest_date]


df = pd.read_csv('flight_data.csv')
wban_iata = pd.read_csv('../Weather Data/emshr_lite.csv')
weather = pd.read_csv('../Weather Data/data/weather_pre.csv')
weather['WBAN'] = weather['STATION'].apply(lambda x: int(x[5:]))
delayed_flight = df[df['DEP_DELAY'] > 15].reset_index(drop=True)
df_flight_time = pd.DataFrame()
df_flight_time['date'] = delayed_flight['FL_DATE']
df_flight_time['time'] = delayed_flight['CRS_DEP_TIME']
df_flight_time['origin'] = delayed_flight['ORIGIN']
df_flight_time['delay'] = delayed_flight['DEP_DELAY']
# convert date and time into datetime format
df_flight_time['time'] = df_flight_time['time'].apply(
    lambda x: str(x)[:-2]+':'+str(x)[-2:]+':00' if x >= 100
    else '00:'+str(x)+':00')
df_flight_time['datetime'] = df_flight_time['date'].map(str) \
                             + '/' + df_flight_time['time']
df_flight_time['datetime'] = pd.to_datetime(
    df_flight_time['datetime'], format='%Y-%m-%d/%H:%M:%S'
)
# merge WBAN codes and IATA codes
df_flight_time = df_flight_time.merge(
    wban_iata,
    left_on='origin',
    right_on='IATA',
    how='inner'
).drop(columns=['origin'])
# only keep the FM-15 and FM-16 type of reports
weather = weather[(weather['REPORTTPYE'] == 'FM-15')
                  | (weather['REPORTTPYE'] == 'FM-16')]
weather['DATE'] = pd.to_datetime(weather['DATE'], format='%Y-%m-%d %H:%M')
res_dict = dict()
minutes_dict = dict()
# pattern of weather types
pattern = re.compile(r'[A-Za-z]{2,}:(\d{2})\s')
# find the weather of the origin airport at closest time moment in weather data
for i in range(df_flight_time.shape[0]):
    match = []
    # if df_flight_time.loc[i, 'WBAN'] == 94850:
    #     continue
    flight_weather = weather.loc[find_closest_date(
        df_flight_time.loc[i, 'datetime'],
        weather[weather['WBAN'] == df_flight_time.loc[i, 'WBAN']].DATE
    )]
    if isinstance(flight_weather['HOURLYPRSENTWEATHERTYPE'], str):
        if re.search(r'\|(([A-Za-z]{2,}:(\d{2})\s)*)\|',
                     flight_weather['HOURLYPRSENTWEATHERTYPE']):
            string = re.search(
                r'\|(([A-Za-z]{2,}:(\d{2})\s)*)\|',
                flight_weather['HOURLYPRSENTWEATHERTYPE']).group(1)
            match = pattern.findall(string)
    if len(match) == 0:
        if 0 in list(res_dict.keys()):
            res_dict[0] += 1
            minutes_dict[0] += df_flight_time.loc[i, 'delay']
        else:
            res_dict[0] = 1
            minutes_dict[0] = df_flight_time.loc[i, 'delay']
    else:
        for num in match:
            if int(num) in list(res_dict.keys()):
                res_dict[int(num)] += 1
                minutes_dict[int(num)] += df_flight_time.loc[i, 'delay']
            else:
                res_dict[int(num)] = 1
                minutes_dict[int(num)] = df_flight_time.loc[i, 'delay']

# calculate average delay minutes for each weather type and plot a histogram
avr_dict = dict()
for i in list(res_dict.keys()):
    avr_dict[i] = minutes_dict[i] / res_dict[i]
weather_type_df = pd.read_csv('../Weather Data/weather_type_codes.csv',
                              sep='\t')
new_avr_dict = dict()
for i in range(weather_type_df.shape[0]):
    if weather_type_df.loc[i, 'weather code'] in list(avr_dict.keys()):
        new_avr_dict[weather_type_df.loc[i, 'weather type']] = avr_dict[
            weather_type_df.loc[i, 'weather code']
        ]
new_avr_df = pd.DataFrame.from_dict(
    new_avr_dict,
    orient='index',
    columns=['average delay minutes']
).sort_values(by='average delay minutes')
new_avr_df.plot(kind='barh',
                title='Average Delay Minutes of Different Weather Types',
                figsize=(10, 7),
                fontsize=14)
