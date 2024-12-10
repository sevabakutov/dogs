from scripts.file_functions import visualise_statistic
from scripts.preprocessing import pred_df_preprocessing
from ml_project.src.scripts.make_predictions import make_predictions
from scripts.statistic import get_dfs, prepare_dataset, train_model, test_model
from utils.get_grades import get_grade_types
from logger import GHLogger

logger = GHLogger()
    
def estimate():
    logger.debug("Getting grades...")
    grades = get_grade_types(data["grade"])

    logger.debug("Getting dist...")
    dist = data["dist"]

    logger.debug("Getting start train...")
    start_train = data["start_train"]
    
    logger.debug("Getting end  train...")
    end_train = data["end_train"]
    
    logger.debug("Getting start test...")
    start_test = data["start_test"]
    
    logger.debug("Getting end test...")
    end_test = data["end_test"]

    logger.debug("Getting dfs...")
    train_df, test_df = get_dfs(dist, start_train, end_train, start_test, end_test)

    logger.debug("Getting train prepared...")
    train_df_prepared = prepare_dataset(train_df, grades)

    logger.debug("Getting test prepared...")
    test_df_prepared = prepare_dataset(test_df, grades)

    logger.debug("Training model...")
    train_model(train_df_prepared, dist, start_train, end_train)

    logger.debug("Testing model...")
    df, pred_pos = test_model(dist, start_train, end_train, test_df_prepared)

    logger.debug("Vis statistic...")
    visualise_statistic(df, pred_pos)