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
