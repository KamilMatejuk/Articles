import const
import datetime
import numpy as np
import pandas as pd


def read_data() -> pd.DataFrame:
    data = pd.read_csv('data.csv')
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    # calculate sums
    for (*cols, total) in [const.COLS_SLEEPING, const.COLS_READING, const.COLS_EXERCISE]:
        data[total] = sum(data[c] for c in cols)
    # shoulder raises
    series, reps, weight, volume = const.COLS_SHOULDER_RAISES
    data[volume] = data[series] * data[reps] * data[weight]
    # energy
    energy = const.COLS_OTHER[4]
    valuemap = { 'low': 1, 'neutral': 2, 'high': 3, np.nan: 0 }
    data[energy] = data[energy].map(valuemap)
    # kcal 7 day moving average
    kcal, kcal_sma = const.COLS_EATING[-2:]
    data[kcal_sma] = data[kcal].replace(0, data[kcal].max() * 0.75).rolling(window=7, min_periods=5).mean().fillna(0)
    return data


def read_passfail() -> pd.DataFrame:
    data = read_data()
    passfail = pd.DataFrame()
    passfail['date'] = data['date']
    # sleep
    sleep_night, sleep_day, sleep_total = const.COLS_SLEEPING
    passfail[sleep_night] = data[sleep_night].map(lambda x: x >= 7 * 60)
    passfail[sleep_day] = data[sleep_day].map(lambda x: x == 0)
    passfail[sleep_total] = data[sleep_total].map(lambda x: x >= 7 * 60)
    # read
    read_total = const.COLS_READING[-1]
    passfail[read_total] = data[read_total].map(lambda x: x >= 5)
    # work
    work_total = const.COLS_WORKING[-1]
    passfail[work_total] = data[work_total].map(lambda x: x >= 15)
    # leisure
    phone, tv = const.COLS_LEISURE
    phone_limit = data['date'].map(lambda x: 3.5 * 60 if x > datetime.datetime(2024, 11, 1) else 4 * 60)
    passfail[phone] = data[phone] < phone_limit
    passfail[tv] = data[tv].map(lambda x: x <= 2 * 60)
    # exercise
    exercise_total = const.COLS_EXERCISE[-1]
    passfail[exercise_total] = data[exercise_total].map(lambda x: x >= 10)
    # shoulder raises
    volume = const.COLS_SHOULDER_RAISES[-1]
    passfail[volume] = data[volume].map(lambda x: x > 0)
    # eat
    kcal, kcal_sma = const.COLS_EATING[-2:]
    kcal_expected = data['date'].map(lambda x: 2500 if x > datetime.datetime(2025, 3, 1) else 2900)
    kcal_limit_min = kcal_expected - 200
    kcal_limit_max = kcal_expected + 200
    passfail[kcal] = (kcal_limit_min < data[kcal]) & (data[kcal] < kcal_limit_max)
    passfail[kcal_sma] = (kcal_limit_min < data[kcal_sma]) & (data[kcal_sma] < kcal_limit_max)
    
    return passfail    