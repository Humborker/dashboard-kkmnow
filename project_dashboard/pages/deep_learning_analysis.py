import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from dataloader import load_project_data
import joblib
import os

# TODO: Hit 80% using scikit machine learning (LOL function)
# TODO: Use deep learning.
# TODO: Use simple scikit machine learning sklearn
path = "../project_dashboard/datasets"
if os.path.exists(path):
    map_df = load_project_data(path)

st.title("Trend_Prediction")

# 1. App Configuration
st.set_page_config(page_title="Trend Predictor")


@st.cache_resource
def load_model():
    return joblib.load("my_model.pkl")


model = load_model()

st.title("ML Model Predictor")

# Example input: Adjust based on your model's features
feature_1 = st.number_input("Enter Feature 1")
feature_2 = st.number_input("Enter Feature 2")

if st.button("Predict"):
    prediction = model.predict([[feature_1, feature_2]])
    st.success(f"The predicted value is: {prediction[0]}")
