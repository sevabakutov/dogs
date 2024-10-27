# диапозон времени ( start_data, end_data)
# дисатнция

import os
import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

from file_functions import load_model
from logger import GHLogger
from settings import ENCODERS_DIR, IMPUTERS_DIR, MODELS_DIR, DATA_DIR, DATASET_DIR

logger = GHLogger("statistic")

def get_dfs(dist, start_date, end_date):
    file_path = os.path.join(DATA_DIR, "train", "datasets", f"dataset_{dist}.0.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, low_memory=False)
    else:
        logger.error(f"Not such file: {file_path}")
        return None

    df['raceDate'] = pd.to_datetime(df['raceDate'], format='%d/%m/%Y')

    result_df = df[(df['raceDate'] >= start_date) & (df['raceDate'] <= end_date)]
    predict_df = df[(df['raceDate'] < start_date) & (df['raceDate'] > end_date)]
    # predict_df.to_csv(os.path.join(DATASET_DIR, "statistic"))

    return result_df, predict_df


def process_dog_data(df):
    dog_names = df['dogName'].unique()

    results = []

    for dog in dog_names:
        dog_data = df[df['dogName'] == dog].sort_values(by='raceDate')

        dog_results = []
        for i, row in dog_data.iterrows():
            current_race_date = row['raceDate']

            previous_races = dog_data[dog_data['raceDate'] < current_race_date].tail(5)

            by = previous_races['resultBtnDistance'].tolist()
            finished = previous_races['resultPosition'].tolist()
            going = previous_races['raceGoing'].tolist()
            price_dens = previous_races['resultPriceDenominator'].tolist()
            price_nums = previous_races['resultPriceNumerator'].tolist()
            race_grade = previous_races['raceClass'].tolist()
            run_time = previous_races['resultRunTime'].tolist()
            trap = previous_races['trapNumber'].tolist()
            weight = previous_races['resultDogWeight'].tolist()
            sec_time = previous_races['resultSectionalTime'].tolist()

            while len(by) < 5:
                by.append(np.nan)
                finished.append(np.nan)
                going.append(np.nan)
                price_dens.append(np.nan)
                price_nums.append(np.nan)
                race_grade.append(np.nan)
                run_time.append(np.nan)
                trap.append(np.nan)
                weight.append(np.nan)
                sec_time.append(np.nan)

            result = (by + finished + going +
                      price_dens + price_nums +
                      race_grade + run_time +
                      trap + weight + sec_time)

            dog_results.append(result)

        dog_data_results = pd.DataFrame(dog_results, columns=[
            'by_1', 'by_2', 'by_3', 'by_4', 'by_5',
            'finished_1', 'finished_2', 'finished_3', 'finished_4', 'finished_5',
            'going_1', 'going_2', 'going_3', 'going_4', 'going_5',
            'price_dens_1', 'price_dens_2', 'price_dens_3', 'price_dens_4', 'price_dens_5',
            'price_nums_1', 'price_nums_2', 'price_nums_3', 'price_nums_4', 'price_nums_5',
            'race_grade_1', 'race_grade_2', 'race_grade_3', 'race_grade_4', 'race_grade_5',
            'run_time_1', 'run_time_2', 'run_time_3', 'run_time_4', 'run_time_5',
            'trap_1', 'trap_2', 'trap_3', 'trap_4', 'trap_5',
            'weight_1', 'weight_2', 'weight_3', 'weight_4', 'weight_5',
            'sec_time_1', 'sec_time_2', 'sec_time_3', 'sec_time_4', 'sec_time_5'
        ])
        dog_data.reset_index(drop=True, inplace=True)
        dog_data_results.reset_index(drop=True, inplace=True)

        combined_data = pd.concat([dog_data, dog_data_results], axis=1)
        results.append(combined_data)

    final_df = pd.concat(results).sort_index()

    return final_df


def fill_miss_values(row):
    last_results = None
    size = None
    start_index = None

    for i in range(2, 6):
        if pd.isna(row[f'finished_{i}']):
            last_results = row[[f'by_{i - 1}', f'finished_{i - 1}',
                                f'going_{i - 1}', f'price_dens_{i - 1}',
                                f'price_nums_{i - 1}', f'race_grade_{i - 1}',
                                f'run_time_{i - 1}', f'trap_{i - 1}',
                                f'weight_{i - 1}', f'sec_time_{i - 1}']]
            size = 5 - i + 1
            start_index = i
            break

    if size is not None:
        for j in range(size):
            idx = start_index + j
            row[f'by_{idx}'] = last_results[f'by_{start_index - 1}']
            row[f'finished_{idx}'] = last_results[f'finished_{start_index - 1}']
            row[f'going_{idx}'] = last_results[f'going_{start_index - 1}']
            row[f'price_dens_{idx}'] = last_results[f'price_dens_{start_index - 1}']
            row[f'price_nums_{idx}'] = last_results[f'price_nums_{start_index - 1}']
            row[f'race_grade_{idx}'] = last_results[f'race_grade_{start_index - 1}']
            row[f'run_time_{idx}'] = last_results[f'run_time_{start_index - 1}']
            row[f'trap_{idx}'] = last_results[f'trap_{start_index - 1}']
            row[f'weight_{idx}'] = last_results[f'weight_{start_index - 1}']
            row[f'sec_time_{idx}'] = last_results[f'sec_time_{start_index - 1}']

    return row


def convert_dist_by(sp):
    try:
        if isinstance(sp, float) and pd.isna(sp):
            return np.nan
        elif isinstance(sp, (int, float)):
            return sp
        elif isinstance(sp, str):
            parts = sp.split()

            if len(parts) == 2:  # Формат "3 3/4"
                whole_part = int(parts[0])
                fraction_part = parts[1]

                if '/' in fraction_part:
                    num, den = fraction_part.split('/')
                    fraction_value = int(num) / int(den)
                    return whole_part + fraction_value
                else:
                    return np.nan

            elif len(parts) == 1:  # Формат "3/4" или "3"
                if '/' in parts[0]:  # Если это дробь
                    num, den = parts[0].split('/')
                    return int(num) / int(den)
                else:  # Если это просто целое число
                    return float(parts[0])
            else:
                return np.nan
        else:
            return np.nan
    except (ValueError, IndexError) as e:
        return np.nan
    except Exception as e:
        return np.nan


def set_adv_lagg(pos, by):
    if by is None or pd.isna(by):
        return np.nan
    result = np.round(by * 0.8, 2) if pos == 1 else np.round(by * -0.8, 2)
    return result


def save_encoder(encoder, dist, start_date, end_date) -> None:
    joblib.dump(encoder, os.path.join(ENCODERS_DIR, f"encoder_{dist}_{start_date}_{end_date}.pkl"))

def save_imputer(imputer, dist, start_date, end_date):
    joblib.dump(imputer, os.path.join(IMPUTERS_DIR, f"imputer_{dist}_{start_date}_{end_date}.pkl"))

def save_model(model, dist, start_date, end_date):
    joblib.dump(model, os.path.join(MODELS_DIR, f"model_{dist}_{start_date}_{end_date}.pkl"))


def prepare_dataset(df, grades):
    print("=====Start======")

    columns_to_drop = ['SP', 'dogBorn', 'dogColour', 'dogId', 'dogSeason',
                       'dogSex', 'dogSire', 'dogSire', 'meetingId',
                       'ownerName', 'raceForecast', 'raceId', 'raceNumber',
                       'raceHandicap', 'racePrizes', 'raceTricast', 'raceType',
                       'resultAdjustedTime', 'resultMarketCnt', 'resultMarketPos',
                       'trainerName', 'trapHandicap', 'raceTime', 'raceTime',
                       'raceDistance', 'resultComment', 'trackName'
                       ]

    df = df.drop(columns_to_drop, axis=1)

    df.replace(['', ' ', np.nan], np.nan)
    df_cleaned = df.dropna(
        subset=['dogName', 'raceClass', 'resultPosition', 'resultPriceDenominator', 'resultPriceNumerator', 'raceDate'])

    print("====First====")
    positions = [1.0 ,2.0, 3.0, 4.0, 5.0, 6.0]
    df_cleaned = df_cleaned[df_cleaned['resultPosition'].isin(positions)]

    if not grades:
        df_cleaned = df_cleaned[~df_cleaned['raceClass'].isin(grades)]

    df_cleaned.loc[:, 'raceDate'] = pd.to_datetime(df_cleaned['raceDate'], format='%d/%m/%Y')
    df_cleaned.loc[:, 'forecast'] = df_cleaned['resultPriceNumerator'] / df_cleaned['resultPriceDenominator']
    df_cleaned = df_cleaned.replace(['', ' ', None], np.nan)

    df_full = process_dog_data(df_cleaned)
    df_full = df_full.replace([None], np.nan)
    df_full = df_full.dropna(subset=['finished_1'])
    df_full = df_full.apply(fill_miss_values, axis=1)
    for i in range(5):
        df_full[f'odds_{i + 1}'] = df_full[f'price_nums_{i + 1}'] / df_full[f'price_dens_{i + 1}']

    columns_to_drop = ['dogName', 'resultBtnDistance',
                       'raceGoing', 'resultPriceDenominator',
                       'resultPriceNumerator', 'resultRunTime', 'resultSectionalTime',
                       'resultDogWeight', 'price_dens_1', 'price_dens_2',
                       'price_dens_3', 'price_dens_4', 'price_dens_5',
                       'price_nums_1', 'price_nums_2', 'price_nums_3',
                       'price_nums_4', 'price_nums_5']
    df_full = df_full.drop(columns_to_drop, axis=1)
    for i in range(5):
        df_full.loc[:, f'by_{i + 1}'] = df_full[f'by_{i + 1}'].apply(convert_dist_by).round(2)
    for i in range(5):
        df_full[f'by_{i + 1}'] = df_full.apply(lambda row: set_adv_lagg(row[f'finished_{i + 1}'], row[f'by_{i + 1}']),
                                               axis=1)

    return df_full



def train_model(df_full, *args):
    columns_cat = ['raceClass', 'race_grade_1', 'race_grade_2', 'race_grade_3', 'race_grade_4', 'race_grade_5']
    df_cat = df_full[columns_cat]
    encoder = OrdinalEncoder()
    encoder.fit(df_cat)

    save_encoder(encoder, *args)

    df_encoded = encoder.transform(df_cat)
    df_encoded_df = pd.DataFrame(df_encoded, columns=columns_cat)
    df_full[columns_cat] = df_encoded_df

    y = df_full['resultPosition']
    df_full = df_full.drop(['resultPosition', 'raceDate'], axis=1)

    print("IMPUTER--------------------------------===============")

    imputer = KNNImputer(n_neighbors=3, weights='distance', keep_empty_features=False)
    imputer.fit(df_full)

    save_imputer(imputer, *args)

    X = imputer.transform(df_full)

    df_ready = pd.DataFrame(X, columns=df_full.columns)

    param_grid = [
        {
            'n_estimators': [100],
            'max_features': [5, 10, 15, 25, 44],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10, 15, 20],
        },
        {
            'bootstrap': [False],
            'n_estimators': [100],
            'max_features': [5, 10, 15, 25, 44],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10, 15, 20],
        }
    ]

    forest_reg = RandomForestClassifier(random_state=42)
    grd_search = GridSearchCV(forest_reg, param_grid, cv=5, scoring='neg_log_loss')
    grd_search.fit(df_ready, y)

    final_model = grd_search.best_estimator_

    save_model(final_model, *args)


def test_model(dist, start_date, end_date, df):
    model = load_model(dist, start_date, end_date)
    df_real_pos_data = df[['resultPosition', 'raceDate']]
    df.drop(['resultPosition', 'raceDate'], axis=1)

    X = df.to_numpy()

    predictions = model.predict_proba(X)

    return df_real_pos_data, predictions
