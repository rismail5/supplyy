import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("delay_model9.pkl")

st.title("🚚 Supply Chain Delay Prediction")

# User inputs
origin = st.selectbox("Origin", ["Delhi", "Mumbai", "Chennai", "Bangalore"])
destination = st.selectbox("Destination", ["Delhi", "Mumbai", "Chennai", "Bangalore"])
shipment_mode = st.selectbox("Shipment Mode", ["Sea", "Road", "Air", "Rail"])
carrier = st.selectbox("Carrier", ["BlueDart", "DHL", "FedEx", "Delhivery"])
weather = st.selectbox("Weather", ["Stormy", "Rainy", "Sunny"])
distance_km = st.number_input("Distance (km)", min_value=1, max_value=5000, value=500)
traffic_level = st.selectbox("Traffic Level", ["Low", "Medium", "High"])
lead_time_days = st.number_input("Lead Time (days)", min_value=1, max_value=30, value=3)
order_weekday = st.selectbox("Order Weekday (0=Mon ... 6=Sun)", list(range(7)))
scheduled_weekday = st.selectbox("Scheduled Weekday (0=Mon ... 6=Sun)", list(range(7)))

# Encode inputs (must match training format)
input_dict = {
    "Distance_km": distance_km,
    "TrafficLevel": {"Low":1, "Medium":2, "High":3}[traffic_level],
    "lead_time_days": lead_time_days,
    "order_weekday": order_weekday,
    "scheduled_weekday": scheduled_weekday,
    "ShipmentMode_Sea": 1 if shipment_mode=="Sea" else 0,
    "ShipmentMode_Road": 1 if shipment_mode=="Road" else 0,
    "ShipmentMode_Air": 1 if shipment_mode=="Air" else 0,
    "ShipmentMode_Rail": 1 if shipment_mode=="Rail" else 0,
    "Carrier_BlueDart": 1 if carrier=="BlueDart" else 0,
    "Carrier_DHL": 1 if carrier=="DHL" else 0,
    "Carrier_FedEx": 1 if carrier=="FedEx" else 0,
    "Carrier_Delhivery": 1 if carrier=="Delhivery" else 0,
    "Weather_Stormy": 1 if weather=="Stormy" else 0,
    "Weather_Rainy": 1 if weather=="Rainy" else 0,
    "Weather_Sunny": 1 if weather=="Sunny" else 0,
    "Origin_Delhi": 1 if origin=="Delhi" else 0,
    "Origin_Mumbai": 1 if origin=="Mumbai" else 0,
    "Origin_Chennai": 1 if origin=="Chennai" else 0,
    "Origin_Bangalore": 1 if origin=="Bangalore" else 0,
    "Destination_Delhi": 1 if destination=="Delhi" else 0,
    "Destination_Mumbai": 1 if destination=="Mumbai" else 0,
    "Destination_Chennai": 1 if destination=="Chennai" else 0,
    "Destination_Bangalore": 1 if destination=="Bangalore" else 0,
}

input_df = pd.DataFrame([input_dict])

# Predict
if st.button("Predict Delay"):
    prediction = model.predict(input_df)[0]
    if prediction == 1:
        st.error("⚠️ Predicted: Delivery will be delayed")
    else:
        st.success("✅ Predicted: Delivery will be on time")
