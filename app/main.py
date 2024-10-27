import sys

from file_functions import visualise_statistic
from statistic import get_dfs, prepare_dataset, train_model
from predict import make_predictions
from preprocessing import pred_df_preprocessing


def get_grade_types(grade_types: str, grades=None):
    if grade_types == "-cus":
        return grades.split(" ")
    if grade_types == "-gen":
        return ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
    if grade_types == "-hp":
        return ['HP']
    if grade_types == "-all":
        return []


def main():
    if len(sys.argv) > 1:

        print(sys.argv)
        match sys.argv[1]:
            case "help":
                print("Руководство:\npython main.py => Всегда начинать писать так. python - это то что запускает main.py (программа)\n"
                      "Третим аргументом может быть:\n\t1) help => помощь\n\t"
                      "2) predict => делает предсказания на день используя заранее оттренерованные модели. Не имеет никаких доп аргументов\n\t"
                      "3) estimate => делает оценку модели. Имеет обязательные доп аргументы. После 'estimate' обязательно следует дистанция, "
                      "нужно написать аргумент '-dist' и затем через пробел дистанцию. "
                      "Далее обязательно указываеться диапозон . Используеться аргумент -date и потом через пробел дата в формате 'dd/mm/yyyy'."
                      "Последний аргумент это грейды. Они могут быть: \n\t-all (все грейды), \n\t-gen (от слова general, основные, от A1 до А10)"
                      ", \n\t-hp (HP), \n\t-cus (кастомные). \nЧтобы прописать желающие грейды, после аргумента cus, нужно открыть двойные кавычки и через пробел прописать грейды.\n\n"
                      "Примеры использования:\n\tpython main.py predict\n\tpython main.py estimate -dist 480 -date 04/06/2024 31/08/2024 -all"
                      "\n\tpython main.py estimate -dist 480 -date 04/06/2024 31/08/2024 -cus 'A2 A6 HP A3' (!!ДВОЙНЫЕ КАВЫЧКИ)!!")

            case "predict":
                dfs_small, dfs_big = pred_df_preprocessing()
                make_predictions(dfs_small)
                make_predictions(dfs_big)

            case "estimate":
                grades = get_grade_types(sys.argv[7])
                train_df, test_df = get_dfs(sys.argv[3], sys.argv[5], sys.argv[6])
                train_df_prepared = prepare_dataset(train_df, grades)
                test_df_prepared = prepare_dataset(test_df, grades)
                train_model(train_df_prepared, sys.argv[3], sys.argv[5], sys.argv[6])
                df, pred_pos = test_df_prepared(sys.argv[3], sys.argv[5], sys.argv[6], test_df_prepared)
                visualise_statistic(df, pred_pos)


    else:
        print("Рома, ты забыл ввести аргументы. python main.py help - для информации")
    
if __name__ == "__main__":
    main()