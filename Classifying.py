import pandas as pd
import numpy as np
import streamlit as st
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Credit Risk Analysis")

# Collect user input
age = st.slider("Age", 20, 80)
house = st.selectbox("Housing Status", ["Owned", "Free", "Rented"])
purpose = st.selectbox("Purpose", ["Car", "Radio/TV", "Furniture/Equipment", "Business", "Education", "Repairs", "Domestic Appliances", "Vacation/Others"])
checking_account = st.selectbox("Current Checking Account Amount:(Little = In-Overdraft - £500, Moderate = £500-£1500, Rich = +£1500)", ["Little", "Moderate", "Rich"])
savings_account = st.selectbox("Current Savings Account Amount: (Little = 0-£500, Moderate = £500-£10000, Rich = +£10000-£30000, Quite Rich = +£30000)", ["Little", "Moderate", "Rich", "Quite Rich"])
credit_amount = st.number_input("Credit Amount Request", min_value=0)
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
    'Purpose For Applying For Credit': [purpose],
    'checking_account_num': [checking_map[checking_account]],
    'saving_accounts_num': [savings_map[savings_account]],
    'Credit amount': [credit_amount],
    'Duration': [duration],
    'credit_repayment_per_month': [credit_amount / duration]
})

job_risk = {0:3, 1:2, 2:1, 3:1}
housing_risk = {'Free':1, 'Rented':2, 'Owned':1}
checking_risk = {0:3, 1:2, 2:1}
saving_risk = {0:3, 1:2, 2:1, 3:1}
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

plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots(figsize=(10,2))

ax.barh(y=0, width=5, left=0, color='green', edgecolor='black', label='Low Risk')
ax.barh(y=0, width=2, left=5, color='orange', edgecolor='black', label='Moderate Risk')
ax.barh(y=0, width=3, left=7, color='red', edgecolor='black', label='High Risk')
              

# Overlay user's score
ax.axvline(score, color='blue', linestyle='--', linewidth=2)
ax.text(score + 0.1, 0.1, f'User Score: {score}', color='blue', fontsize=12)

# Formatting
ax.set_xlim(2, 10)
ax.set_ylim(-0.5, 0.5)
ax.set_yticks([])
ax.set_title('User Credit Risk Position on Risk Scale', fontsize=14)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=3, frameon=False)


st.pyplot(fig)

st.subheader("Suggestions to Reduce Credit Risk")

suggestions = []

if job in [0, 1]:
    suggestions.append("📌 Consider applying for skilled roles to reduce occupational risk.")

if house == "Rented":
    suggestions.append("📌 Owning or living rent-free is considered lower risk than renting.")

if checking_map[checking_account] < 2 or savings_map[savings_account] < 3:
    suggestions.append("📌 Increase checking account balance and build savings to improve financial resilience.")

if credit_amount > 5000:
    suggestions.append("📌 Reducing the requested credit amount may improve repayment ratio.")

for tip in suggestions:
    st.markdown(tip)


def recalculate_score_with_improvements(row):
    improved = row.copy()

    # Apply hypothetical improvements
    improved['Job'] = max(row['Job'], 2)  # Assume user moves to Skilled
    improved['Housing'] = 'Owned' if row['Housing'] == 'Rented' else row['Housing']
    improved['checking_account_num'] = max(row['checking_account_num'], 2)
    improved['saving_accounts_num'] = max(row['saving_accounts_num'], 3)
    improved['Credit amount'] = min(row['Credit amount'], 5000)
    improved['Duration'] = min(row['Duration'], 24)
    improved['credit_repayment_per_month'] = improved['Credit amount'] / improved['Duration']

    # Recalculate score
    new_score = 0
    new_score += job_risk.get(improved['Job'], 2)
    new_score += housing_risk.get(improved['Housing'], 2)
    new_score += checking_risk.get(improved['checking_account_num'], 2)
    new_score += saving_risk.get(improved['saving_accounts_num'], 2)

    if improved['credit_repayment_per_month'] >= repayment_threshold:
        new_score += 1
    if improved['Age'] >= 65 and improved['Duration'] > 24:
        new_score += 1
    if duration_threshold < improved['Duration'] < upper_duration_threshold:
        new_score -= 1
    if improved['Duration'] >= upper_duration_threshold:
        new_score -= 2

    return new_score, improved['credit_repayment_per_month'], improved['Duration']

new_score, new_repayment, new_duration = recalculate_score_with_improvements(input_data.iloc[0])

st.subheader("Impact of Suggested Improvements")
st.write(f"🔄 New Risk Score: {new_score}")
st.write(f"🔄 New Risk Level: {categorise_risk(new_score)}")
st.write(f"💰 New Monthly Repayment: £{new_repayment:.2f}")
st.write(f"📆 New Duration: {new_duration} months")
st.success(f"✅ Your credit risk score has improved to {new_score} — now classified as {categorise_risk(new_score)}.")


st.subheader("Duration To Repay Affects on Credit & Monthly Payments")

duration_threshold = 18.0
upper_duration_threshold = 24.0
durations = [6, 12, 18, 24, 30]
monthly_repayments = []
risk_scores = []

checking_account_num = checking_map[checking_account]
saving_accounts_num = savings_map[savings_account]

for duration in durations:
    repayment = credit_amount / duration
    score = job_risk[job] + housing_risk[house] + checking_risk[checking_account_num] + saving_risk[saving_accounts_num]

    if repayment >= repayment_threshold:
        score += 1
    if age >= 65 and duration > 24:
        score += 1
    if duration > duration_threshold and duration < upper_duration_threshold:
        score -= 1
    if duration >= upper_duration_threshold:
        score -= 2

    monthly_repayments.append(repayment)
    risk_scores.append(score)

# Plotting dual-axis chart
plt.style.use('seaborn-v0_8')
fig, ax1 = plt.subplots(figsize=(10, 6))
x = np.arange(len(durations))

# Left axis: Monthly repayment bars
bars = ax1.bar(x, monthly_repayments, color='tab:green', width=0.6, label='Monthly Repayment (£)')
ax1.set_ylabel('Monthly Repayment (£)', color='tab:green')
ax1.tick_params(axis='y', labelcolor='tab:green')

# Annotate repayment bars
for i, bar in enumerate(bars):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f"£{monthly_repayments[i]:.2f}", ha='center', fontsize=9)

# Right axis: Risk score line
ax2 = ax1.twinx()
ax2.plot(x, risk_scores, color='tab:red', marker='o', linewidth=2, label='Risk Score')
ax2.set_ylabel('Risk Score', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# X-axis and title
ax1.set_xticks(x)
ax1.set_xticklabels(durations)
ax1.set_xlabel('Repayment Duration (months)')
fig.suptitle(f'Monthly Repayment vs Risk Score by Duration\nCredit Amount: £{credit_amount}', fontsize=14)

# Legends
# Add bottom-left label for Monthly Repayment axis
fig.text(0.1, 0.02, 'Monthly Repayment (£)', ha='left', va='center', fontsize=11, color='tab:green')

# Add bottom-right label for Risk Score axis
fig.text(0.9, 0.02, 'Risk Score', ha='right', va='center', fontsize=11, color='tab:red')


st.pyplot(fig)

st.info("ℹ️ Shorter durations increase monthly repayment but may reduce credit risk. This chart shows how both metrics shift across repayment terms.")

