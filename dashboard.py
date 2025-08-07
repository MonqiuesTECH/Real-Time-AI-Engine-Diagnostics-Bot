import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("EngineMind – Real-Time Engine Telemetry")

import time

st.subheader("Telemetry Time-Series (Live)")

placeholder = st.empty()
features = ['rpm', 'temperature', 'pressure', 'vibration']
sim_df = pd.read_csv("telemetry_simulated.csv")

for i in range(10, len(sim_df), 5):
    window = sim_df.iloc[i-10:i]
    with placeholder.container():
        st.line_chart(window[features])
        st.caption(f"Latest timestamp: {window.iloc[-1]['timestamp']}")
    time.sleep(1)
df = sim_df
st.subheader("Failure Events")
failures = df[df['failure'] == 1]
st.write(failures if not failures.empty else "No failures detected.")

from predict import predict_failure

st.subheader("Failure Prediction")

latest = df.iloc[-1][['rpm', 'temperature', 'pressure', 'vibration']].to_dict()
prob = predict_failure(latest)

st.metric("Failure Risk", f"{prob * 100:.1f} %")

if prob > 0.8:
    st.error("⚠️ High Failure Risk! Immediate attention required.")
elif prob > 0.5:
    st.warning("⚠️ Moderate risk. Monitor closely.")
else:
    st.success(" Engine appears stable.")
import base64
from report_generator import generate_pdf

report_data = latest.copy()
report_data["Failure Probability"] = f"{prob*100:.1f}%"
generate_pdf(report_data, "engine_report.pdf")

with open("engine_report.pdf", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
    href = f'<a href="data:file/pdf;base64,{b64}" download="EngineReport.pdf">📄 Download Diagnostic Report</a>'
    st.markdown(href, unsafe_allow_html=True)
import streamlit as st

if st.secrets.get("password") and st.text_input("Password", type="password") != st.secrets["password"]:
    st.stop()
