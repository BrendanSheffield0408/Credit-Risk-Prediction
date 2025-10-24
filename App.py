import pandas as pd
import numpy as np
import streamlit as st
import joblib


# Load models and preprocessing pipeline
tree_model = joblib.load('best_dt.pkl')
preprocessor = joblib.load('preprocessor.pkl')
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer



st.title("Credit Risk Prediction")

# Collect user input
age = st.slider("Age", 20, 80)
house = st.selectbox("Housing Status", ["own", "free", "rent"])
purpose = st.selectbox("Purpose", ["car", "radio/TV", "furniture/equipment", "business", "education", "repairs", "domestic appliances", "vacation/others"])
checking_account = st.selectbox("Current Checking Account Amount", ["Little", "Moderate", "Rich"])
savings_account = st.selectbox("Current Savings Account Amount", ["Little", "Moderate", "Rich", "Quite Rich"])
credit_amount = st.number_input("Credit Amount", min_value=0)
duration = st.number_input("Number of Months Till Repayment", min_value=1)
# Add other features as needed...

# Create input DataFrame
input_data = pd.DataFrame({
    'Age': [age],
    'Housing': [house],
    'Purpose': [purpose],
    'Checking account': [checking_account],
    'Savings accounts': [savings_account],
    'Credit amount': [credit_amount],
    'Duration': [duration],
    'credit_repayment_per_month': [credit_amount / duration]
})


# Preprocess input
X_input = preprocessor.transform(input_data)

# Predict
#log_pred = log_model.predict_proba(X_input)[0][1]
tree_pred = tree_model.predict_proba(X_input)[0][1]

st.subheader("Prediction Scores")
st.write(f"Decision Tree: {tree_pred:.2f}")
def risk_label(score):
    if score > 0.7:
        return "High Risk 🔴"
    elif score > 0.4:
        return "Moderate Risk 🟠"
    else:
        return "Low Risk 🟢"

st.write(f"Risk Level: {risk_label(tree_pred)}")

