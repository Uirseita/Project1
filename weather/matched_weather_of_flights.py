import numpy as np
import pandas as pd
from datetime import timedelta


def find_closest_date(timepoint, time_series):
    # takes a pd.Timestamp() instance and a pd.Series with dates in it
    # calcs the delta between `timepoint` and each date in `time_series`
    # returns the closest date and optionally
    # the number of days in its time delta
    timepoint = np.datetime64(timepoint)
    deltas = np.abs(np.subtract(time_series.values, timepoint))
    idx_closest_date = np.argmin(deltas)
    return time_series.index[idx_closest_date]


def match_weather_data():
    # read flight data
    df = pd.read_csv('flight_data.csv')
    # p = 1  # p% of lines
    # filename = 'flight_data.csv'
    # random.seed(234)
    #
    # # if random from [0,1] > p, skip row
    # df = pd.read_csv(
    #          filename,
    #          header=0,
    #          skiprows=lambda i: i>0 and random.random() > p/100
    # )

    # clean flight data
    airport_lst = ['TKI']
    tail_num_lst = ['PLANET', 'N101NK', 'N999FR', 'N700TA', 'N187SW', 'N399FR']
    df = df[(~df['ORIGIN'].isin(airport_lst))
            & (~df['TAIL_NUM'].isin(tail_num_lst))]

    # read wban_iata and weather data
    wban_iata = pd.read_csv('../Weather Data/wban_to_iata.csv')
    weather = pd.read_csv('../Weather Data/data/weather_pre.csv')
    weather['WBAN'] = weather['STATION'].apply(lambda x: int(x[5:]))

    # convert string into datetime
    df['dep_time'] = df['CRS_DEP_TIME'].apply(
        lambda x: str(x)[:-2]+':'+str(x)[-2:]+':00'
        if x >= 100 else '00:'+str(x)+':00')
    df['dep_datetime'] = df['FL_DATE'].map(str) + '/' + df['dep_time']
    df['dep_datetime'] = pd.to_datetime(
        df['dep_datetime'], format='%Y-%m-%d/%H:%M:%S')
    df['arr_time'] = df['CRS_ARR_TIME'].apply(
        lambda x: str(x)[:-2]+':'+str(x)[-2:]+':00'
        if x >= 100 else '00:'+str(x)+':00')
    df['arr_datetime'] = df['FL_DATE'].map(str) + '/' + df['arr_time']
    df['arr_datetime'] = pd.to_datetime(
        df['arr_datetime'], format='%Y-%m-%d/%H:%M:%S')

    # add 1 day for flights overnight
    df.arr_datetime = df[
        ['CRS_DEP_TIME', 'CRS_ARR_TIME', 'arr_datetime']
    ].apply(
        lambda x: x[2] + timedelta(days=1) if x[0] - x[1] >= 600 else x[2],
        axis=1)

    df = df.merge(
        wban_iata, left_on='ORIGIN', right_on='IATA', how='inner'
    ).drop(columns=['IATA']).rename(columns={'WBAN':'origin_WBAN'})
    df = df.merge(
        wban_iata, left_on='DEST', right_on='IATA', how='inner'
    ).drop(columns=['IATA']).rename(columns={'WBAN':'dest_WBAN'})

    #     origin weather index
    grouped = weather.groupby('WBAN')
    df = df.sort_values(by=['origin_WBAN', 'dep_datetime']).reset_index(
        drop=True)
    df['origin_weather_index'] = np.nan
    wban = -1
    df['dep_datetime'] = df[['origin_WBAN', 'dep_datetime']].apply()

    for i in range(df.shape[0]):
        if wban != df.loc[i, 'origin_WBAN']:
            weather_series = grouped.get_group(df.loc[i, 'origin_WBAN']).DATE
            wban = df.loc[i, 'origin_WBAN']
        else:
            pass
        df.loc[i, 'origin_weather_index'] = find_closest_date(
            df.loc[i, 'dep_datetime'], weather_series)

    #     dest weather index
    df = df.sort_values(by=['dest_WBAN', 'arr_datetime']).reset_index(
        drop=True)
    df['dest_weather_index'] = np.nan
    wban = -1
    for i in range(df.shape[0]):
        if wban != df.loc[i, 'dest_WBAN']:
            weather_series = grouped.get_group(df.loc[i, 'dest_WBAN']).DATE
            wban = df.loc[i, 'dest_WBAN']
        else:
            pass
        df.loc[i, 'dest_weather_index'] = find_closest_date(
            df.loc[i, 'arr_datetime'], weather_series)
    df = df.sort_index()
    return df
