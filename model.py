# model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model(csv_path="telemetry_simulated.csv"):
    df = pd.read_csv(csv_path)
    features = ['rpm', 'temperature', 'pressure', 'vibration']
    target = 'failure'

    model = RandomForestClassifier(n_estimators=100)
    model.fit(df[features], df[target])
    joblib.dump(model, "failure_model.pkl")

def load_model():
    return joblib.load("failure_model.pkl")
