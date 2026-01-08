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
    # Create DataFrame from input
    df = pd.DataFrame([payload])
    
    # Define categorical columns
    categorical_cols = ["Fuel_Type", "Seller_Type", "Transmission", "Owner", "Car_Name"]
    
    # One-hot encode categorical columns
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    
    # Create a DataFrame with all training columns initialized to 0
    df_final = pd.DataFrame(0, index=df_encoded.index, columns=_feature_columns)
    
    # Fill in the values for columns that exist in the input
    for col in df_encoded.columns:
        if col in _feature_columns:
            df_final[col] = df_encoded[col]
    
    # Ensure correct column order and data types
    df_final = df_final[_feature_columns].astype(float)
    
    return df_final


def predict_price(payload: dict) -> float:
    """Predict car price given input payload."""
    load_artifacts()
    X = preprocess(payload)
    pred = _model.predict(X)[0]
    return float(pred)