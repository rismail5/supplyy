import streamlit as st
import pandas as pd
import joblib

model = joblib.load('delay_model.pkl')
st.title("Supply Chain Delay Prediction Dashboard")

uploaded_file = st.file_uploader("Upload shipment data", type=["xlsx"])
if uploaded_file:
    data = pd.read_excel(uploaded_file)
    data_encoded = pd.get_dummies(data)
    prediction = model.predict(data_encoded)
    st.write(prediction)
