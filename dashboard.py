import streamlit as st
import pandas as pd
import numpy as np
import time

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
import time

st.sidebar.header("Live Stream Controls")
refresh_sec = st.sidebar.slider("Refresh rate (seconds)", 0.2, 2.0, 1.0, 0.1)
window_size = st.sidebar.slider("Chart window (rows)", 20, 200, 60, 5)
step_size   = st.sidebar.slider("Step size (rows/frame)", 1, 20, 5, 1)
inject_faults = st.sidebar.checkbox("Inject fault pattern (demo)")

sim_df = pd.read_csv("telemetry_simulated.csv")

if "stream_idx" not in st.session_state:
    st.session_state.stream_idx = window_size

st.subheader("Telemetry Time-Series (Live)")
placeholder = st.empty()

st.session_state.stream_idx = min(
    len(sim_df),
    st.session_state.stream_idx + step_size
)

view_end = st.session_state.stream_idx
view_start = max(0, view_end - window_size)
window = sim_df.iloc[view_start:view_end].copy()

if inject_faults and len(window) >= 10:
    ramp = np.linspace(0, 12, len(window))
    window["temperature"] = window["temperature"] + ramp
    window["vibration"] = window["vibration"] + (ramp * 0.01)

with placeholder.container():
    st.line_chart(window[["rpm", "temperature", "pressure", "vibration"]])
    st.caption(f"Latest timestamp: {window.iloc[-1]['timestamp']}  •  Rows: {view_end}/{len(sim_df)}")

time.sleep(refresh_sec)
st.rerun()

df = sim_df

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
