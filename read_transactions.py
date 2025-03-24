import pandas as pd

df = pd.read_csv("transactions.csv")
df["Date"] = pd.to_datetime(df["Date"])

print(df.head())
