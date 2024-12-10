import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import joblib
import hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
from settings import DATA_DIR, MODELS_DIR, IMPUTERS_DIR, ENCODERS_DIR

from logger import GHLogger

logger = GHLogger()


def generate_file_name(params):
    params_str = "_".join(map(str, params))
    hash_object = hashlib.md5(params_str.encode())
    file_name = hash_object.hexdigest()
    return file_name


def is_csv_file_empty(file_path: str) -> bool:
    return os.path.getsize(file_path) == 0


def get_pred_file() -> str:
    dir_path = os.path.join(DATA_DIR, "to_pred")
    date = datetime.today()
    date = date.strftime('%Y-%m-%d')
    file_path = os.path.join(dir_path, f'to_pred_{date}.csv')
    return file_path


def load_dataset(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)


def save_final_file(df: pd.DataFrame) -> None:
    df.to_csv(os.path.join(DATA_DIR, "temp.csv"))


def get_final_file() -> str:
    return os.path.join(DATA_DIR, "temp.csv")

def load_model(dist, start_date=None, end_date=None, grade=None):
    logger.debug("Loading model...")

    if grade:
        file_path = os.path.join(MODELS_DIR, "random_forest_class", f'model_{dist}_{grade}.pkl')
    elif start_date:
        file_path = os.path.join(MODELS_DIR, "random_forest_class", f'model_{dist}_{start_date}_{end_date}.pkl')
    else:
        file_path = os.path.join(MODELS_DIR, "random_forest_class", f'model_{dist}.pkl')

    if os.path.exists(file_path):
        return joblib.load(file_path)

    return None

def load_imputer(dist, start_date=None, end_date=None, grade=None):
    logger.debug("Loading imputer...")

    if grade:
        file_path = os.path.join(IMPUTERS_DIR, f'imputer_{dist}_{grade}.pkl')
    elif start_date:
        file_path = os.path.join(IMPUTERS_DIR, f'imputer_{dist}_{start_date}_{end_date}.pkl')
    else:
        file_path = os.path.join(IMPUTERS_DIR, f'imputer_{dist}.pkl')

    if os.path.exists(file_path):
        return joblib.load(file_path)

    return None

def load_encoder(dist, start_date=None, end_date=None, grade=None):
    logger.debug("Loading encoder...")

    if grade:
        file_path = os.path.join(ENCODERS_DIR, f'encoder_{dist}_{grade}.pkl')
    elif start_date:
        file_path = os.path.join(ENCODERS_DIR, f'encoder_{dist}_{start_date}_{end_date}.pkl')
    else:
        file_path = os.path.join(ENCODERS_DIR, f'encoder_{dist}.pkl')

    if os.path.exists(file_path):
        return joblib.load(file_path)

    return None


def save_race_results_to_pdf(race_results, name: str, grade=None) -> None:
    logger.debug("Saving results to a PDF file...")

    dir_path = os.path.join(DATA_DIR, "results")
    os.makedirs(dir_path, exist_ok=True)
    filename = os.path.join(dir_path, name)

    with PdfPages(filename) as pdf:
        grouped_results = {}

        for _, (row, predictions) in enumerate(zip(race_results[0].itertuples(index=False), race_results[1])):
            try:
                race_time = datetime.strptime(row.race_date_time, '%Y-%m-%d %H:%M')
            except ValueError as e:
                logger.exception(f"Error parsing date: {e}")
                race_time = row.race_date_time

            race_distance = row.raceDistance
            dog_name = row.name

            probabilities = np.round(predictions, 2)

            if race_time not in grouped_results:
                grouped_results[race_time] = {'race_distance': race_distance, 'dogs': []}

            grouped_results[race_time]['dogs'].append({
                'Dog Name': dog_name,
                '1st place': probabilities[0],
                '2nd place': probabilities[1],
                '3rd place': probabilities[2],
                '4th place': probabilities[3],
                '5th place': probabilities[4],
                '6th place': probabilities[5]
            })

        for race_time, race_info in grouped_results.items():
            race_distance = race_info['race_distance']
            dogs = race_info['dogs']

            df = pd.DataFrame(dogs)

            fig, ax = plt.subplots(figsize=(10, len(dogs) * 0.5 + 2))
            ax.axis('tight')
            ax.axis('off')
            ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
            if grade:
                title = f"Race on {race_time}, Distance: {race_distance}m, {grade}"
            else:
                title = f"Race on {race_time}, Distance: {race_distance}m"
            ax.set_title(title)

            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)

def visualise_statistic(df: pd.DataFrame, pred_positions):
    p_len = df.size
    real_positions = df['resultPosition'].values

    mistakes = []
    for start in range(0, p_len, 100):
        end = start + 100 if start + 100 < p_len else p_len
        m_val = 0
        for pos, p in zip(real_positions[start:end], pred_positions[start:end]):
            if pos == 1 and (p == 4 or p == 5 or p == 6):
                m_val += 1
        mistakes.append(m_val)

    x_labels = range(1, len(mistakes) + 1, 1)
    plt.bar(x_labels, mistakes, width=0.6, align='center', edgecolor='black')
    plt.ylabel("Кол-во ошибок")
    plt.xlabel(
        f"Koл-во соток: кол-во предсказаний({p_len}) / 100 = кол-во соток({len(mistakes)})\nОбщий процент ошибки = {p_len / sum(mistakes)}%")
    plt.yticks(range(0, max(mistakes) + 2, 1))
    plt.xticks(range(0, len(mistakes) + 2, 1))
    for x, y in zip(x_labels, mistakes):
        plt.text(x, y + 0.2, f"{y}%", ha='center', va='bottom')

    plt.show()