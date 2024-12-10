from make_predictions import make_predictions
from preprocessing import pred_df_preprocessing

if __name__ == "__main__":
    dfs_small, dfs_big = pred_df_preprocessing()
    make_predictions(dfs_small)
    make_predictions(dfs_big)