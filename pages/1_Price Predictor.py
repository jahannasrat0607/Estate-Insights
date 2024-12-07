import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load data and model
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)
with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

# Page Configurations
st.set_page_config(page_title="Real Estate", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS for better UI
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
            font-family: 'Arial', sans-serif;
        }
        .main-container {
            padding: 2rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        h1 {
            color: #4CAF50;
            text-align: center;
            margin-bottom: 2rem;
        }
        label {
            font-size: 1rem;
            color: #333333;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            border-radius: 5px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .prediction {
            font-size: 1.2rem;
            color: #4CAF50;
            text-align: center;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<h1>Property Price Prediction</h1>", unsafe_allow_html=True)

# Input Fields
st.subheader("Enter Your Inputs")

property_type = st.selectbox("Property Type", ['flat', 'house'])
sector = st.selectbox("Sector", sorted(df['sector'].unique().tolist()))
bedrooms = float(st.selectbox("Number of Bedrooms", sorted(df['bedRoom'].unique().tolist())))
bathrooms = float(st.selectbox("Number of Bathrooms", sorted(df['bathroom'].unique().tolist())))
balcony = st.selectbox("Balconies", sorted(df['balcony'].unique().tolist()))
property_age = st.selectbox("Property Age", sorted(df['agePossession'].unique().tolist()))
built_up_area = float(st.number_input("Built-Up Area (in sq. ft.)"))
servant_room = float(st.selectbox("Servant Room", [0.0, 1.0]))
store_room = float(st.selectbox("Store Room", [0.0, 1.0]))
furnishing_type = st.selectbox("Furnishing Type", sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox("Luxury Category", sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox("Number of Floors", sorted(df['floor_category'].unique().tolist()))

# Prediction Button and Output
if st.button("Predict"):
    # Prepare DataFrame
    data = [[property_type, sector, bedrooms, bathrooms, balcony, property_age, built_up_area,
             servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']
    one_df = pd.DataFrame(data, columns=columns)

    # Predict
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    # Display Result
    st.markdown(f"<div class='prediction'>The estimated price of this property is between <b>{round(low, 2)} Cr</b> and <b>{round(high, 2)} Cr</b>.</div>", unsafe_allow_html=True)

# Close main container
st.markdown("</div>", unsafe_allow_html=True)
