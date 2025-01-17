import hashlib
import os
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from settings import DATA_DIR, MODELS_DIR, IMPUTERS_DIR, ENCODERS_DIR
import joblib


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
    print(file_path)
    return file_path


def load_dataset(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)


def save_final_file(df: pd.DataFrame) -> None:
    df.to_csv(os.path.join(DATA_DIR, "temp.csv"))


def get_final_file() -> str:
    return os.path.join(DATA_DIR, "temp.csv")

def load_model(dist, start_date=None, end_date=None, grade=None):
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
    print('received: ', race_results)
    dir_path = os.path.join(DATA_DIR, "results")
    filename = os.path.join(dir_path, name)

    with PdfPages(filename) as pdf:
        # Для каждого уникального времени гонки собираем данные
        grouped_results = {}

        for idx, (row, predictions) in enumerate(zip(race_results[0].itertuples(index=False), race_results[1])):
            # Преобразуем строку с датой и временем в объект datetime
            try:
                race_time = datetime.strptime(row.race_date_time, '%Y-%m-%d %H:%M')
            except ValueError as e:
                print(f"Error parsing date: {e}")
                race_time = row.race_date_time  # В случае ошибки используем строковое представление

            race_distance = row.raceDistance
            dog_name = row.name

            # Собираем вероятности для каждого места
            probabilities = np.round(predictions, 2)

            # Если гонка уже есть, добавляем результаты, иначе создаем новую запись
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

        # Теперь для каждой гонки создаем таблицу
        for race_time, race_info in grouped_results.items():
            race_distance = race_info['race_distance']
            dogs = race_info['dogs']

            # Создаем DataFrame для всей гонки
            df = pd.DataFrame(dogs)

            fig, ax = plt.subplots(figsize=(10, len(dogs) * 0.5 + 2))  # Зависимость высоты от количества строк
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