import streamlit as st
import requests

# Backend API URL (use env var or default to local)
import os
API_URL = os.getenv("API_URL", "http://localhost:8000/predict")

st.set_page_config(page_title="Purchase Predictor", page_icon="🛍️")

st.title("🛍️ Purchase Value Predictor")
st.write("Enter customer details below to predict their purchase value.")

# Input fields
age = st.number_input("Age", min_value=18, max_value=100, value=30)
income = st.number_input("Income ($)", min_value=0, value=50000, step=1000)

if st.button("Predict Purchase Value"):
    # Prepare payload
    payload = {
        "age": age,
        "income": income
    }
    
    with st.spinner("Analyzing..."):
        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                value = result['predicted_purchase_value']
                
                # Determine customer segment
                if value < 150:
                    segment = "Low Value"
                    color = "red"
                elif value < 300:
                    segment = "Medium Value"
                    color = "orange"
                else:
                    segment = "High Value"
                    color = "green"
                
                # Display results
                st.success("Prediction Completed!")
                st.metric(label="Predicted Purchase Value", value=f"${value:,.2f}")
                st.markdown(f"**Customer Segment:** :{color}[**{segment}**]")
                
            else:
                st.error(f"Error from API: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to backend server. Please ensure it is running.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
