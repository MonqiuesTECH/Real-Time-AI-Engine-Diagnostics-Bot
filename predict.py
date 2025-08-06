import pandas as pd
import joblib
import os

def load_model():
    if os.path.exists("failure_model.pkl"):
        return joblib.load("failure_model.pkl")
    return None

model = load_model()

def predict_failure(data_row):
    features = ['rpm', 'temperature', 'pressure', 'vibration']
    df = pd.DataFrame([data_row], columns=features)

    if model:
        try:
            return round(model.predict_proba(df)[0][1], 3)
        except:
            return 0.0
    return 0.25
