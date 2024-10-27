from datetime import datetime
import pandas as pd
import pytz
import re
import ast



def convert_sp_to_numeric(odds) -> list:
    odds_clean = list()
    
    for sp in odds:
        sp_clean = re.sub(r'[^0-9/]', '', sp)
        if '/' in sp_clean:
            numerator, denominator = sp_clean.split('/')
            if denominator != '0':
                sp_clean = float(numerator) / float(denominator) + 1
                odds_clean.append(sp_clean)

    return odds_clean


def convert_et_to_cet(et_time_str):
    et_timezone = pytz.timezone('US/Eastern')
    cet_timezone = pytz.timezone('Europe/Madrid')

    et_time = datetime.strptime(et_time_str, '%H:%M ET')

    now = datetime.now()
    et_time = et_time.replace(year=now.year, month=now.month, day=now.day)

    et_time = et_timezone.localize(et_time)

    cet_time = et_time.astimezone(cet_timezone)

    time = cet_time.strftime('%d/%m/%Y %H:%M:%S')

    return time


def convert_yards_to_meters(yards):
    return int(yards * 0.9144)


def load_and_convert_temp_file():
    df = pd.read_csv(r'C:\machine learning\gb_greyhound\grayhound\data\pred\temp.csv')

    df['names'] = df['names'].apply(lambda x: [name.capitalize() for name in ast.literal_eval(x)])
    df['odds'] = df['odds'].apply(lambda x: convert_sp_to_numeric(ast.literal_eval(x)))
    df['time'] = df['time'].apply(convert_et_to_cet)
    df['dist'] = df['dist'].apply(convert_yards_to_meters)

    df = df[df.apply(lambda row: len(row['names']) == len(row['odds']), axis=1)]

    return df