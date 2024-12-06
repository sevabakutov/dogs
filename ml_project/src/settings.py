import os.path
import environ

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ENCODERS_DIR = os.path.join(DATA_DIR, "encoders")
IMPUTERS_DIR = os.path.join(DATA_DIR, "imputers")
MODELS_DIR = os.path.join(DATA_DIR, "models")
DATASET_DIR = os.path.join(DATA_DIR, "train", "datasets")


env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, "..", ".env"))