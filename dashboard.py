import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import base64
from report_generator import generate_pdf


st.set_page_config(layout="wide")
st.title("ZARI – Real-Time Engine Telemetry")
if "authed" not in st.session_state:
    st.session_state.authed = False

def login_gate():
    if st.session_state.authed:
    
        with st.sidebar:
            if st.button("Log out"):
                st.session_state.authed = False
                st.rerun()
        return  

    st.title("🔐 EngineMind Login")
    user = st.text_input("Username")
    pw   = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == st.secrets["auth"]["username"] and pw == st.secrets["auth"]["password"]:
            st.session_state.authed = True
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop() 
if "play" not in st.session_state:
    st.session_state.play = True

st.sidebar.toggle("Play", key="play", value=st.session_state.play)
if st.sidebar.button("Reset stream"):
    st.session_state.stream_idx = window_size

login_gate()

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
play = st.sidebar.toggle("Play", value=True)
reset = st.sidebar.button("Reset stream")
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
    st.error("⚠ High Failure Risk! Immediate attention required.")
elif prob > 0.5:
    st.warning("🟠 Moderate risk. Monitor closely.")
else:
    st.success("✅ Engine appears stable.")

company = "EngineMind"
footer = "Powered by ZARI – Confidential"

report_data = latest.copy()
report_data["Failure Probability"] = f"{prob*100:.1f}%"

pdf_name = f"engine_report_{datetime.utcnow().strftime('%Y%m%d-%H%M%SZ')}.pdf"
generate_pdf(report_data, pdf_name, company, footer)

with open(pdf_name, "rb") as f:
    pdf_bytes = f.read()

st.download_button(
    label="⬇️ Download Diagnostic Report",
    data=pdf_bytes,
    file_name=pdf_name,
    mime="application/pdf",
)

