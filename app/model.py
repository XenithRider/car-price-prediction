from pathlib import Path
import pandas as pd
import joblib

CAR_PRICE_API_DIR = Path(__file__).resolve().parent
MODEL_PATH = CAR_PRICE_API_DIR / "random_forest_model.pkl"
COLS_PATH = CAR_PRICE_API_DIR / "feature_columns.pkl"
print(COLS_PATH)
_model = None
_feature_columns = None


def load_artifacts():
    global _model, _feature_columns
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    if _feature_columns is None:
        _feature_columns = joblib.load(COLS_PATH)



