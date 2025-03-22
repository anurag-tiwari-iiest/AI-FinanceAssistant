import os
import joblib
import pandas as pd

if not os.path.exists("transactions.csv"):
    raise FileNotFoundError("❌ Error: 'transactions.csv' not found!")

if not os.path.exists("transaction_classifier.pkl") or not os.path.exists("vectorizer.pkl"):
    raise FileNotFoundError("❌ Error: Classifier model or vectorizer missing! Run 'train_classifier.py' first.")

model = joblib.load("transaction_classifier.pkl")
vectorizer = joblib.load("vectorizer.pkl")

df = pd.read_csv("transactions.csv")

X_test = vectorizer.transform(df["Description"])
df["Category"] = model.predict(X_test)

unknown_categories = df[df["Category"].isna()]
if not unknown_categories.empty:
    print("⚠ Warning: Some transactions could not be categorized. Review them manually.")
    print(unknown_categories)
df["Category"] = df["Category"].fillna("Uncategorized")

df.to_csv("categorized_transactions.csv", index=False)
print("✅ Categorization complete! Saved to 'categorized_transactions.csv'")
