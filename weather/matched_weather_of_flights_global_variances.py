import numpy as np
import pandas as pd
from datetime import timedelta


def find_closest_date(lst):
    # take a row of 2 columns: wban and time
    # find the matched index in weather
    global wban
    global weather_series
    global grouped
    if wban != lst[0]:
        weather_series = grouped.get_group(lst[0]).DATE
        wban = lst[0]
    else:
        pass
    timepoint = np.datetime64(lst[1])
    deltas = np.abs(np.subtract(weather_series.values, timepoint))
    idx_closest_date = np.argmin(deltas)
    return weather_series.index[idx_closest_date]


def match_weather_data(df1):
    #     origin weather index
    df1 = df1.sort_values(by=['origin_WBAN', 'dep_datetime']).reset_index(
        drop=True)
    df1['origin_weather_index'] = np.nan
    df1 = df1.sort_values(by=['origin_WBAN', 'dep_datetime']).reset_index(
        drop=True)
    df1['origin_weather_index'] = df1[['origin_WBAN', 'dep_datetime']].apply(
        lambda x: find_closest_date(x), axis=1)
    #     destination weather index
    df1 = df1.sort_values(by=['dest_WBAN', 'arr_datetime']).reset_index(
        drop=True)
    df1['dest_weather_index'] = df1[['dest_WBAN', 'arr_datetime']].apply(
        lambda x: find_closest_date(x), axis=1)
    df1 = df1.sort_index()
    return df1


if __name__ == "__main__":
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
    weather = pd.read_csv('../Weather Data/data/weather_pre.csv'
                          , parse_dates=['DATE'])
    weather['WBAN'] = weather['STATION'].apply(lambda x: int(x[5:]))

    # convert string into datetime
    df['dep_time'] = df['CRS_DEP_TIME'].apply(
        lambda x: str(x)[:-2] + ':' + str(x)[-2:] + ':00'
        if x >= 100 else '00:' + str(x) + ':00')
    df['dep_datetime'] = df['FL_DATE'].map(str) + '/' + df['dep_time']
    df['dep_datetime'] = pd.to_datetime(
        df['dep_datetime'], format='%Y-%m-%d/%H:%M:%S')
    df['arr_time'] = df['CRS_ARR_TIME'].apply(
        lambda x: str(x)[:-2] + ':' + str(x)[-2:] + ':00'
        if x >= 100 else '00:' + str(x) + ':00')
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
    ).drop(columns=['IATA']).rename(columns={'WBAN': 'origin_WBAN'})
    df = df.merge(
        wban_iata, left_on='DEST', right_on='IATA', how='inner'
    ).drop(columns=['IATA']).rename(columns={'WBAN': 'dest_WBAN'})

    grouped = weather.groupby('WBAN')
    weather_series = pd.Series()
    wban = -1
    df = match_weather_data(df)
