import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Verify that the required file exists
if not os.path.exists("categorized_transactions.csv"):
    raise FileNotFoundError("❌ Error: 'categorized_transactions.csv' not found! Run 'categorize_expenses.py' first.")

df = pd.read_csv("categorized_transactions.csv")
df['Transaction_Type'] = np.where(df['Amount'] < 0, 'Debit', 'Credit')

df['Transaction_Hour'] = pd.to_datetime(df['Date'], errors='coerce').dt.hour

df['Transaction_Amount'] = df['Amount'].abs()

df = pd.get_dummies(df, columns=['Transaction_Type'], drop_first=True)

features = ['Transaction_Amount', 'Transaction_Hour', 'Transaction_Type_Debit']

scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])

contamination_rate = 0.03

# Train anomaly detection model
model = IsolationForest(contamination=contamination_rate, random_state=42)
df["Model_Fraud_Flag"] = model.fit_predict(df[features])

large_amount_threshold = 3
df['Large_Amount_Flag'] = np.where(df['Transaction_Amount'] > large_amount_threshold, 1, 0)

df['Odd_Hour_Flag'] = np.where((df['Transaction_Type_Debit'] == 1) & 
                               ((df['Transaction_Hour'] < 6) | (df['Transaction_Hour'] > 22)), 1, 0)

df['Final_Fraud'] = np.where((df['Model_Fraud_Flag'] == -1) | 
                             (df['Large_Amount_Flag'] == 1) | 
                             (df['Odd_Hour_Flag'] == 1), 1, 0)

df['Final_Fraud'] = np.where(df['Amount'] > 0, 0, df['Final_Fraud'])

fraudulent = df[df["Final_Fraud"] == 1]

fraudulent.to_csv("fraud_transactions.csv", index=False)

print(f"✅ Fraud detection complete! {len(fraudulent)} transactions flagged as suspicious.")