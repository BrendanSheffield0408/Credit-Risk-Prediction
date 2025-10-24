import pandas as pd
import numpy as np
import streamlit as st
import joblib
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
job = st.selectbox("Current Occupation/Residency (0: Untrained & Non-Resident, 1: Untrained & Resident, 2: Trained/Skilled, 3: High Skilled)", [0,1,2,3])
# Add other features as needed...

checking_map = {'Little': 0, 'Moderate': 1, 'Rich': 2}
savings_map = {'Little': 0, 'Moderate': 1, 'Rich': 2, 'Quite Rich': 3}


# Collect user input
input_data = pd.DataFrame({
    'Age': [age],
    'Job': [job],
    'Housing': [house],
    'Purpose': [purpose],
    'checking_account_num': [checking_map[checking_account]],
    'saving_accounts_num': [savings_map[savings_account]],
    'Credit amount': [credit_amount],
    'Duration': [duration],
    'credit_repayment_per_month': [credit_amount / duration]
})

job_risk = {0:3, 1:2, 2:1, 3:1}
housing_risk = {'free':1, 'rent':2, 'own':1}
checking_risk = {1:3, 2:2, 3:1}
saving_risk = {1:3, 2:2, 3:1, 4:1}
repayment_threshold = 130.33
duration_threshold = 18.0
upper_duration_threshold = 24.0


st.subheader("Prediction Credit Scores")
def calculate_risk_score(row):
  score = 0
  score += job_risk.get(row['Job'],2)
  score += housing_risk.get(row['Housing'],2)
  score += checking_risk.get(row['checking_account_num'],2)
  score += saving_risk.get(row['saving_accounts_num'],2)

  if row['credit_repayment_per_month'] >= repayment_threshold:
    score += 1
  if row['Age'] >= 65 and row['Duration'] > 24:
    score += 1
  if row['Duration'] > duration_threshold and row['Duration'] < upper_duration_threshold:
    score -= 1
  if row['Duration'] > duration_threshold and row['Duration'] >= upper_duration_threshold:
    score -= 2
  return score 

def categorise_risk(score):
    if score >= 6 and score < 8:
        return "🟠 Moderate Risk"
    elif score < 6:
        return "🟢 Low Risk"
    else:
        return "🔴 High Risk"


score = calculate_risk_score(input_data.iloc[0])
st.write(f"Risk Score: {score}")
st.write(f"Risk Level: {categorise_risk(score)")
