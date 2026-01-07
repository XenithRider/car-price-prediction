from pathlib import Path
import pandas as pd
import joblib

CAR_PRICE_API_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = CAR_PRICE_API_DIR / "random_forest_model.pkl"
COLS_PATH = CAR_PRICE_API_DIR / "feature_columns.pkl"

_model = None
_feature_columns = None


def load_artifacts():
    """Load model and feature columns only once."""
    global _model, _feature_columns

    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)

    if _feature_columns is None:
        if not COLS_PATH.exists():
            raise FileNotFoundError(f"Feature columns file not found at {COLS_PATH}")
        _feature_columns = joblib.load(COLS_PATH)


def preprocess(payload: dict) -> pd.DataFrame:
    """
    Converts raw input into the SAME one-hot encoded column structure used in training.
    Ensures missing columns are added and extra columns are dropped.
    """
    df = pd.DataFrame([payload])

    categorical_cols = ["Fuel_Type", "Seller_Type", "Transmission", "Owner", "Car_Name"]
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Add missing columns
    for col in _feature_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    # Keep only training columns, in correct order
    df_encoded = df_encoded[_feature_columns]

    return df_encoded


def predict_price(payload: dict) -> float:
    """Predict car price given input payload."""
    load_artifacts()
    X = preprocess(payload)
    pred = _model.predict(X)[0]
    return float(pred)