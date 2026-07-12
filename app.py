import streamlit as st
import pandas as pd
import joblib

# Load model
try:
    model = joblib.load("delay_model12.pkl")
except Exception as e:
    st.error(f"Model failed to load: {e}")


st.title("📦 Delivery Delay Prediction")

# Inputs
origin = st.selectbox("Origin", ["Delhi", "Mumbai", "Chennai", "Bangalore"])
destination = st.selectbox("Destination", ["Ahmedabad", "Hyderabad", "Kolkata", "Pune"])
shipment_mode = st.selectbox("Shipment Mode", ["Sea", "Road", "Air", "Rail"])
carrier = st.selectbox("Carrier", ["BlueDart", "DHL", "FedEx", "Delhivery"])
weather = st.selectbox("Weather", ["Stormy", "Rainy", "Sunny"])
distance_km = st.number_input("Distance (km)", min_value=1, max_value=5000, value=500)
traffic_level = st.selectbox("Traffic Level", ["Low", "Medium", "High"])
lead_time_days = st.number_input("Lead Time (days)", min_value=1, max_value=30, value=3)
order_weekday = st.selectbox("Order Weekday (0=Mon ... 6=Sun)", list(range(7)))
scheduled_weekday = st.selectbox("Scheduled Weekday (0=Mon ... 6=Sun)", list(range(7)))

# Encode inputs
input_dict = {
    "Distance_km": distance_km,
    "TrafficLevel": {"Low":1, "Medium":2, "High":3}[traffic_level],
    "order_weekday": order_weekday,
    "scheduled_weekday": scheduled_weekday,
    "lead_time_days": lead_time_days,
    "ShipmentMode_Air": 1 if shipment_mode=="Air" else 0,
    "ShipmentMode_Rail": 1 if shipment_mode=="Rail" else 0,
    "ShipmentMode_Road": 1 if shipment_mode=="Road" else 0,
    "ShipmentMode_Sea": 1 if shipment_mode=="Sea" else 0,
    "Carrier_BlueDart": 1 if carrier=="BlueDart" else 0,
    "Carrier_DHL": 1 if carrier=="DHL" else 0,
    "Carrier_Delhivery": 1 if carrier=="Delhivery" else 0,
    "Carrier_FedEx": 1 if carrier=="FedEx" else 0,
    "Weather_Rainy": 1 if weather=="Rainy" else 0,
    "Weather_Stormy": 1 if weather=="Stormy" else 0,
    "Weather_Sunny": 1 if weather=="Sunny" else 0,
    "Origin_Bangalore": 1 if origin=="Bangalore" else 0,
    "Origin_Chennai": 1 if origin=="Chennai" else 0,
    "Origin_Delhi": 1 if origin=="Delhi" else 0,
    "Origin_Mumbai": 1 if origin=="Mumbai" else 0,
    "Destination_Ahmedabad": 1 if destination=="Ahmedabad" else 0,
    "Destination_Hyderabad": 1 if destination=="Hyderabad" else 0,
    "Destination_Kolkata": 1 if destination=="Kolkata" else 0,
    "Destination_Pune": 1 if destination=="Pune" else 0,
}

# Reorder columns to match training dataset
expected_order = [
    "Distance_km",
    "TrafficLevel",
    "order_weekday",
    "scheduled_weekday",
    "lead_time_days",
    "ShipmentMode_Air",
    "ShipmentMode_Rail",
    "ShipmentMode_Road",
    "ShipmentMode_Sea",
    "Carrier_BlueDart",
    "Carrier_DHL",
    "Carrier_Delhivery",
    "Carrier_FedEx",
    "Weather_Rainy",
    "Weather_Stormy",
    "Weather_Sunny",
    "Origin_Bangalore",
    "Origin_Chennai",
    "Origin_Delhi",
    "Origin_Mumbai",
    "Destination_Ahmedabad",
    "Destination_Hyderabad",
    "Destination_Kolkata",
    "Destination_Pune",
]

input_df = pd.DataFrame([input_dict])[expected_order]

# Predict
if st.button("Predict Delay"):
    try:
        prediction = model.predict(input_df)[0]
        if prediction == 1:
            st.error("⚠️ Predicted: Delivery will be delayed")
        else:
            st.success("✅ Predicted: Delivery will be on time")
    except Exception as e:
        st.warning(f"Prediction failed: {e}")


