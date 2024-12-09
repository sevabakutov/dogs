import os
import re
import json
import numpy as np
import pandas as pd
import random

from settings import DATA_DIR
from logger import GHLogger
from scripts.file_functions import get_pred_file, load_dataset
from crawling.scripts.race_spider import start_race_spider

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = GHLogger()


def convert_dist_by(dist_by):
    try:
        if isinstance(dist_by, float) and pd.isna(dist_by):
            return np.nan
        elif isinstance(dist_by, (float, int)):
            return dist_by
        elif isinstance(dist_by, str):
            if dist_by.isdigit():
                return float(dist_by)

            match = re.match(r"(\d*)&frac(\d)(\d)", dist_by)
            if match:
                whole_part = int(match.group(1)) if match.group(1) else 0
                num = int(match.group(2))
                den = int(match.group(3))
                return whole_part + num / den
            else:
                return np.nan
        else:
            return np.nan
    except (ValueError, IndexError) as e:
        logger.exception(f"Error processing value '{dist_by}': {e}")
        return np.nan
    except Exception as e:
        logger.exception(f"Unexpected error processing value '{dist_by}': {e}")
        return np.nan
        
def set_adv_lagg(pos, by):
    if by is None or pd.isna(by):
        return np.nan
    result = np.round(by * 0.8, 2) if pos == 1 else np.round(by * -0.8, 2)
    return result

def convert_dist_to_int(dist):
    try:
        if isinstance(dist, str):
            cleaned_dist = re.sub(r'[^\d]', '', dist)
            if cleaned_dist:
                result = int(cleaned_dist)
                return result
            else:
                logger.error(f"String '{dist}' could not be converted to integer")
                return np.nan
        elif isinstance(dist, float) and pd.isna(dist):
            return np.nan
        elif isinstance(dist, (int, float)):
            return dist
        else:
            logger.error(f"Unsupported type: {type(dist)}, expected str, int, or float")
            return np.nan

    except Exception as e:
        logger.exception(f"Unexpected error occurred while converting distance: {e}")
        return np.nan
    
def convert_forecast(sp):
    try:
        if isinstance(sp, str):
            sp = re.sub(r'[^\d/]', '', sp)
            if sp:
                if '/' not in sp:
                    result = int(sp)
                    return result
                else:
                    try:
                        num, den = sp.split('/')
                        result = int(num) / int(den)
                        return result
                    except ValueError:
                        logger.error(f"Invalid fraction format in string: {sp}")
                        return np.nan
            else:
                logger.error(f"String '{sp}' could not be converted to a number")
                return np.nan
        elif isinstance(sp, float) and pd.isna(sp):
            return np.nan
        elif isinstance(sp, (int, float)):
            return sp
        else:
            logger.error(f"Unsupported type: {type(sp)}, expected str, int, or float")
            return np.nan

    except Exception as e:
        logger.exception(f"Unexpected error occurred while converting forecast: {e}")
        return np.nan
    
def convert_going(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        return np.nan


def filter_df_big(df: pd.DataFrame) -> dict:
    file_name = os.path.join(DATA_DIR, "json", "dist_classes.json")
    with open(file_name, mode='r') as file:
        classes = json.load(file)

    dfs = {distance: sub_df.groupby('raceClass') if distance == 480 else sub_df
           for distance, sub_df in df.groupby('raceDistance')}

    new_dfs = {}

    for dist, df_ in dfs.items():
        dist = str(dist)

        if dist in classes:
            cls = classes[dist]
            df_ = df_[df_['raceClass'].isin(cls)]

            for i in range(5):
                column_name = f'race_grade_{i + 1}'
                column_names = [f'by_{i + 1}', f'finished_{i + 1}', f'going_{i + 1}',
                    f'run_time_{i + 1}', f'trap_{i + 1}', f'weight_{i + 1}', f'sec_time_{i + 1}']

                df_[column_name] = df_[column_name].apply(lambda x: random.choice(cls) if x not in cls else x)

                df_.loc[~df_[column_name].isin(cls), column_names] = np.nan

            new_dfs[dist] = df_
    new_dfs[480] = dfs[480]

    return new_dfs


def filter_df_small(df: pd.DataFrame) -> dict:
    file_name = os.path.join(DATA_DIR, "json", "dist_classes.json")
    with open(file_name, mode='r') as file:
        classes = json.load(file)

    dfs = {distance: sub_df for distance, sub_df in df.groupby('raceDistance')}

    new_dfs = {}

    for dist, df_ in dfs.items():
        dist = str(dist)

        if dist in classes:
            cls = classes[dist]
            df_ = df_[df_['raceClass'].isin(cls)]

            for i in range(5):
                column_name = f'race_grade_{i + 1}'
                column_names = [f'by_{i + 1}', f'finished_{i + 1}', f'going_{i + 1}',
                    f'run_time_{i + 1}', f'trap_{i + 1}', f'weight_{i + 1}']

                df_[column_name] = df_[column_name].apply(lambda x: random.choice(cls) if x not in cls else x)

                df_.loc[~df_[column_name].isin(cls), column_names] = np.nan

            new_dfs[dist] = df_

    return new_dfs


def pred_df_preprocessing() -> dict:
    logger.debug("Preparing data frame for predictions\n")
    
    try:
        pred_filename = get_pred_file()
        if not os.path.exists(pred_filename):
            logger.debug("Crawling page with races has started.\n")
            start_race_spider()
            logger.debug("Crawling page with races has finished.")
            

        if not os.path.exists(pred_filename):
            logger.error(f"'pred_filename': {pred_filename}: incorrect path!")
            return {}

        logger.debug("Loading dataset")
        df = load_dataset(pred_filename)

        logger.debug("Dropping rows with NaN in raceDistance")
        df.dropna(subset=['raceDistance'], axis=0, inplace=True)

        logger.debug("Preparing 'By_' columns")
        for i in range(5):
            df.loc[:, f'by_{i+1}'] = df[f'by_{i+1}'].apply(convert_dist_by).round(2)

        for i in range(5):
            df[f'by_{i + 1}'] = df[f'by_{i + 1}'].astype('float64')

        for i in range(5):
            df[f'by_{i+1}'] = df.apply(
                lambda row: set_adv_lagg(row[f'finished_{i+1}'], row[f'by_{i+1}']),
                axis=1
            )

        logger.debug("Preparing column 'distances'")
        for i in range(5):
            df.loc[:, f'dist_{i+1}'] = df[f'dist_{i+1}'].apply(convert_dist_to_int)
        df.loc[:, 'raceDistance'] = df[f'raceDistance'].apply(convert_dist_to_int)

        logger.debug("Preparing column 'forecast'")
        df.loc[:, 'forecast'] = df['forecast'].apply(convert_forecast)
        for i in range(5):
            df.loc[:, f'odds_{i+1}'] = df[f'odds_{i+1}'].apply(convert_forecast)

        logger.debug("Preparing column 'going'")
        for i in range(5):
            df.loc[:, f'going_{i + 1}'] = df[f'going_{i + 1}'].apply(convert_going)

        logger.debug("Dropping columns 'comment_'")
        df = df.drop(['comments', 'comnt_1', 'comnt_2', 'comnt_3', 'comnt_4', 'comnt_5', 'trackName'], axis=1)

        logger.debug("Spliting main data frame into two data frames.")
        df_small = df[df['raceDistance'] <= 305]
        df_big = df[df['raceDistance'] > 305]
        df_small = df_small[
            ['raceClass', 'trapNumber', 'forecast', 
                    'by_1', 'by_2', 'by_3', 'by_4', 'by_5',
                    'finished_1', 'finished_2', 'finished_3', 'finished_4', 'finished_5',
                    'going_1', 'going_2', 'going_3', 'going_4', 'going_5',
                    'race_grade_1', 'race_grade_2', 'race_grade_3', 'race_grade_4', 'race_grade_5',
                    'run_time_1', 'run_time_2', 'run_time_3', 'run_time_4', 'run_time_5',
                    'trap_1', 'trap_2', 'trap_3', 'trap_4', 'trap_5',
                    'weight_1', 'weight_2', 'weight_3', 'weight_4', 'weight_5',
                    'odds_1', 'odds_2', 'odds_3', 'odds_4', 'odds_5', 'raceDistance', 'race_date_time', 'name'
            ]
        ]
        df_big = df_big[
            ['raceClass', 'trapNumber', 'forecast',
             'by_1', 'by_2', 'by_3', 'by_4', 'by_5',
             'finished_1', 'finished_2', 'finished_3', 'finished_4', 'finished_5',
             'going_1', 'going_2', 'going_3', 'going_4', 'going_5',
             'race_grade_1', 'race_grade_2', 'race_grade_3', 'race_grade_4', 'race_grade_5',
             'run_time_1', 'run_time_2', 'run_time_3', 'run_time_4', 'run_time_5',
             'trap_1', 'trap_2', 'trap_3', 'trap_4', 'trap_5',
             'weight_1', 'weight_2', 'weight_3', 'weight_4', 'weight_5',
             'sec_time_1', 'sec_time_2', 'sec_time_3', 'sec_time_4', 'sec_time_5',
             'odds_1', 'odds_2', 'odds_3', 'odds_4', 'odds_5', 'raceDistance', 'race_date_time', 'name'
             ]
        ]

        logger.debug("Filetring dataframe with distance <= 305")
        dfs_small = filter_df_small(df_small)

        logger.debug("Filetring dataframe with distance > 305")
        dfs_big = filter_df_big(df_big)

        logger.debug("Filter passed success!")
        return dfs_small, dfs_big

    except Exception as e:
        logger.exception(f"Unexpected error in pred_df_preprocessing: {e}")
        return {}
