import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="centered",
)

# --- Header ---
st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
        }
        .sub-caption {
            text-align: center;
            color: #555;
            font-size: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="main-title">🚗 Car Price Prediction</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-caption">Enter car details below and get an instant prediction of its selling price.</p>',
    unsafe_allow_html=True,
)

API_URL = "https://car-price-prediction-o3xf.onrender.com/predict" or "http://127.0.0.1:8080/predict"  

# --- Input Section ---
st.header("📋 Car Details")

col1, col2 = st.columns(2)

with col1:
    car_name = st.text_input("Car Name", value="swift", help="e.g. swift, ritz, sx4")
    year = st.number_input("Year", min_value=1990, max_value=2026, value=2014, step=1)
    present_price = st.number_input(
        "Present Price (in lakhs)", min_value=0.0, value=5.59, step=0.1
    )
    kms_driven = st.number_input("Kms Driven", min_value=0, value=40000, step=1000)

with col2:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    owner_label = st.selectbox(
        "Owner", ["0 (First Owner)", "1 (Second Owner)", "3 (Third Owner)"]
    )
    owner = int(owner_label.split()[0])

# --- Payload Preview ---
payload = {
    "Car_Name": str(car_name),
    "Year": int(year),
    "Present_Price": float(present_price),
    "Kms_Driven": int(kms_driven),
    "Fuel_Type": str(fuel_type),
    "Seller_Type": str(seller_type),
    "Transmission": str(transmission),
    "Owner": int(owner),
}

with st.expander("🔍 View Payload Being Sent"):
    st.json(payload)

# --- Prediction Button ---
st.markdown("---")
if st.button("💰 Predict Price"):
    with st.spinner("Connecting to API and predicting..."):
        try:
            res = requests.post(API_URL, json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                # Fixed: Use the correct key from your PredictionResponse model
                pred = data.get("prediction_price")

                if pred is None:
                    st.warning("⚠️ API responded but prediction key not found.")
                    st.json(data)
                else:
                    st.success(f"✅ Predicted Selling Price: **₹ {pred:.2f} lakhs**")
            else:
                st.error(f"❌ API Error {res.status_code}")
                st.code(res.text)
        except requests.exceptions.RequestException as e:
            st.error("❌ Could not connect to API. Is FastAPI running?")
            st.code(str(e))

# --- Footer ---
st.markdown(
    """
    <hr>
    <p style="text-align:center; color:gray; font-size:0.9rem;">
        Built with ❤️ using FastAPI + Streamlit
    </p>
    """,
    unsafe_allow_html=True,
)