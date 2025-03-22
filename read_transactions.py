import pandas as pd

# Load CSV
df = pd.read_csv("transactions.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Display first few transactions
print(df.head())
