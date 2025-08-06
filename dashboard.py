import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("EngineMind – Real-Time Engine Telemetry")

df = pd.read_csv("telemetry_simulated.csv")

st.subheader("Telemetry Time-Series")
st.line_chart(df[['rpm', 'temperature', 'pressure', 'vibration']])

st.subheader("Failure Events")
failures = df[df['failure'] == 1]
st.write(failures if not failures.empty else "No failures detected.")
