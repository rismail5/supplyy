import streamlit as st
import pandas as pd
import pickle

# Load dataset
df = pd.read_excel("supply_chain_data.xlsx")

# Convert date columns to numerical features (ordinal dates)
df['OrderDate'] = df['OrderDate'].apply(lambda x: x.toordinal() if pd.notna(x) else 0)
df['ScheduledDeliveryDate'] = df['ScheduledDeliveryDate'].apply(lambda x: x.toordinal() if pd.notna(x) else 0)
df['ActualDeliveryDate'] = df['ActualDeliveryDate'].apply(lambda x: x.toordinal() if pd.notna(x) else 0)

# Load trained model
with open("delay_model3.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Supply Chain Delay Prediction Dashboard")

# Sidebar inputs
origin = st.selectbox("Select Origin", df["Origin"].unique())
destination = st.selectbox("Select Destination", df["Destination"].unique())
shipment_mode = st.selectbox("Select Shipment Mode", df["ShipmentMode"].unique())
carrier = st.selectbox("Select Carrier", df["Carrier"].unique())
weather = st.selectbox("Select Weather", df["Weather"].unique())
traffic = st.selectbox("Select Traffic Level", df["TrafficLevel"].unique())
distance = st.slider("Distance (km)", int(df["Distance_km"].min()), int(df["Distance_km"].max()))

order_date = st.date_input("Order Date")
scheduled_date = st.date_input("Scheduled Delivery Date")
actual_date = st.date_input("Actual Delivery Date")

# Prepare input row
input_data = pd.DataFrame({
    "Origin":[origin],
    "Destination":[destination],
    "Distance_km":[distance],
    "ShipmentMode":[shipment_mode],
    "Carrier":[carrier],
    "Weather":[weather],
    "TrafficLevel":[traffic],
    "OrderDate":[order_date.toordinal()],
    "ScheduledDeliveryDate":[scheduled_date.toordinal()],
    "ActualDeliveryDate":[actual_date.toordinal()]
})

# One-hot encode categorical variables
input_encoded = pd.get_dummies(input_data)

# Align with training features
train_features = pd.get_dummies(df.drop("DelayDays", axis=1))
input_encoded = input_encoded.reindex(columns=train_features.columns, fill_value=0)

# Prediction
prediction = model.predict(input_encoded)[0]

st.write("### Prediction Result:")
st.success("Delayed" if prediction==1 else "On Time")
