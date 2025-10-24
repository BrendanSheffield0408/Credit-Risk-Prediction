import pandas as pd
import numpy as np
import streamlit as st
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Credit Risk Prediction")

# Collect user input
age = st.slider("Age", 20, 80)
house = st.selectbox("Housing Status", ["Own", "Free", "Rent"])
purpose = st.selectbox("Purpose", ["Car", "Radio/TV", "Furniture/Equipment", "Business", "Education", "Repairs", "Domestic Appliances", "Vacation/Others"])
checking_account = st.selectbox("Current Checking Account Amount: (Little = In-Overdraft - £500, Moderate = £500-£1500, Rich = +£1500)", ["Little", "Moderate", "Rich"])
savings_account = st.selectbox("Current Savings Account Amount: (Little = 0-£500, Moderate = £500-£10000, Rich = +£10000-£30000, Quite Rich = +£30000)", ["Little", "Moderate", "Rich", "Quite Rich"])
credit_amount = st.number_input("Credit Amount", min_value=0)
duration = st.number_input("Minimum Number of Months Till Repayment", min_value=1)
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
st.write(f"Risk Level: {categorise_risk(score)}")

plt.style.use('seaborn-v0_8)
fig, ax = plt.subplots(fig_size=(10,2))

ax.barh(y=0, width=5, left=0, color='green', edgecolor='black', label='Low Risk')
ax.barh(y=0, width=2, left=5, color='orange', edgecolor='black', label='Moderate Risk')
ax.barh(y=0, width=3, left=7, color='red', edgecolor='black', label='High Risk')
              

# Overlay user's score
ax.axvline(score, color='blue', linestyle='--', linewidth=2)
ax.text(user_score + 0.1, 0.1, f'User Score: {score}', color='blue', fontsize=12)

# Formatting
ax.set_xlim(0, 10)
ax.set_ylim(-0.5, 0.5)
ax.set_yticks([])
ax.set_xlabel('Credit Risk Score (0 = Low Risk, 10 = High Risk)', fontsize=12)
ax.set_title('User Credit Risk Position on Risk Scale', fontsize=14)
ax.legend(loc='upper right')

# Save figure
output_path = "/mnt/data/credit_risk_score_chart.png"
plt.tight_layout()
plt.savefig(output_path)
plt.close()

output_path
