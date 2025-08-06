# predict.py
import pandas as pd
from model import load_model

model = load_model()

def predict_failure(data_row):
    features = ['rpm', 'temperature', 'pressure', 'vibration']
    input_df = pd.DataFrame([data_row], columns=features)
    prob = model.predict_proba(input_df)[0][1]
    return round(prob, 3)
