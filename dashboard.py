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
