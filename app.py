import streamlit as st
import pandas as pd
import joblib

# Load dataset
df = pd.read_excel("supply_chain_data.xlsx")

# Load trained model
model = joblib.load("delay_model.pkl")

st.title("Supply Chain Delay Prediction Dashboard")

# Sidebar inputs
origin = st.selectbox("Select Origin", df["Origin"].unique())
destination = st.selectbox("Select Destination", df["Destination"].unique())
shipment_mode = st.selectbox("Select Shipment Mode", df["ShipmentMode"].unique())
carrier = st.selectbox("Select Carrier", df["Carrier"].unique())
weather = st.selectbox("Select Weather", df["Weather"].unique())
traffic = st.selectbox("Select Traffic Level", df["TrafficLevel"].unique())
distance = st.slider("Distance (km)", int(df["Distance_km"].min()), int(df["Distance_km"].max()))

# Prepare input row
input_data = pd.DataFrame({
    "Origin":[origin],
    "Destination":[destination],
    "Distance_km":[distance],
    "ShipmentMode":[shipment_mode],
    "Carrier":[carrier],
    "Weather":[weather],
    "TrafficLevel":[traffic]
})

# One-hot encode categorical variables to match training
input_encoded = pd.get_dummies(input_data)

# Align with training columns
train_features = pd.get_dummies(df.drop("DelayDays", axis=1))
input_encoded = input_encoded.reindex(columns=train_features.columns, fill_value=0)

# Prediction
prediction = model.predict(input_encoded)[0]

st.write("### Prediction Result:")
st.success("Delayed" if prediction==1 else "On Time")
