import re
import pandas as pd

from datetime import timedelta, datetime
from scripts.file_functions import save_race_results_to_pdf, load_model, load_imputer, load_encoder
from logger import GHLogger

logger = GHLogger()

def make_predictions(dfs):
    logger.debug("Make predictions")
    columns_cat = ['raceClass', 'race_grade_1', 'race_grade_2', 'race_grade_3', 'race_grade_4', 'race_grade_5']

    try:
        for dist, df in dfs.items():
            dist = int(dist)

            if dist == 480:
                for grade, df_480 in df:
                    df_480 = df_480.drop(columns_cat, axis=1)

                    if grade == 'HP':
                        df_480 = df_480.drop(['sec_time_1', 'sec_time_2', 'sec_time_3', 'sec_time_4', 'sec_time_5'], axis=1)

                    if re.match(r'^OR.*', grade):
                        encoder = load_encoder(dist=dist, grade=grade)
                        if not encoder:
                            logger.error(f"Not encoder for distance: {dist}, grade: {grade}")
                            continue

                        df_cat = df[columns_cat]
                        df_encoded = encoder.transform(df_cat)
                        df_encoded_df = pd.DataFrame(df_encoded, columns=columns_cat)
                        df[columns_cat] = df_encoded_df

                    imputer = load_imputer(dist=dist, grade=grade)
                    if not imputer:
                        logger.debug(f"Not imputer for distance: {dist}, grade: {grade}")
                        continue

                    model = load_model(dist=dist, grade=grade)
                    if not model:
                        logger.debug(f"Not model for distance: {dist}, grade: {grade}")
                        continue

                    df_nrr = df_480[['name', 'raceDistance', 'race_date_time']]
                    df_480 = df_480.drop(['name', 'raceDistance', 'race_date_time'], axis=1)

                    X = imputer.transform(df_480)
                    predictions = model.predict_proba(X)

                    race_results = (df_nrr, predictions)

                    date = datetime.today() + timedelta(days=1)
                    date = date.strftime('%Y-%m-%d')
                    name = f"predictions_{dist}_{date}_{grade}.pdf"

                    save_race_results_to_pdf(race_results, name, grade)

            else:                
                encoder = load_encoder(dist)
                if not encoder:
                    logger.error(f"Not encoder for distance: {dist}")
                    continue

                df_cat = df[columns_cat]
                df_encoded = encoder.transform(df_cat)
                df_encoded_df = pd.DataFrame(df_encoded, columns=columns_cat)
                df[columns_cat] = df_encoded_df

                imputer = load_imputer(dist)
                if not imputer:
                    logger.debug(f"Not imputer for distance: {dist}")
                    continue

                model = load_model(dist)
                if not model:
                    logger.debug(f"Not model for distance: {dist}")
                    continue

                df_nrr = df[['name', 'raceDistance', 'race_date_time']]
                df = df.drop(['name', 'raceDistance', 'race_date_time'], axis=1)

                X = imputer.transform(df)
                predictions = model.predict_proba(X)

                race_results = (df_nrr, predictions)

                date = datetime.today() + timedelta(days=1)
                date = date.strftime('%Y-%m-%d')
                name = f"predictions_{dist}_{date}.pdf"

                save_race_results_to_pdf(race_results, name)

    except Exception as ex:
        logger.exception(f"{ex}, DISTANCE: {dist}")