import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# Expanded dataset with more transactions
data = {
    "Description": [
        "Amazon Purchase", "Uber Ride", "McDonald's", "Salary", "Rent Payment", "Grocery Shopping",
        "Starbucks Coffee", "Car Repair", "Gym Membership", "Netflix Subscription",
        "Walmart Shopping", "Electricity Bill", "Water Bill", "Gas Station", "Movie Ticket",
        "Flight Ticket", "Hotel Booking", "Train Ticket", "Doctor Visit", "Medicine Purchase",
        "Insurance Payment", "Restaurant Dinner", "Fast Food", "Loan Payment", "Gift Purchase",
        "Concert Ticket", "Parking Fee", "Online Course", "Spotify Subscription", "Clothing Purchase",
        "Electronics Purchase", "Furniture Purchase", "Home Decor", "Books Purchase", "Pet Supplies",
        "Charity Donation", "Tax Payment", "Lottery Ticket", "Home Cleaning Service", "Babysitting Service"
    ],
    "Category": [
        "Shopping", "Transport", "Food & Dining", "Income", "Housing", "Groceries",
        "Food & Dining", "Auto & Transport", "Health & Fitness", "Entertainment",
        "Shopping", "Utilities", "Utilities", "Auto & Transport", "Entertainment",
        "Travel", "Travel", "Travel", "Healthcare", "Healthcare",
        "Insurance", "Food & Dining", "Food & Dining", "Loans", "Shopping",
        "Entertainment", "Auto & Transport", "Education", "Entertainment", "Shopping",
        "Shopping", "Shopping", "Home Improvement", "Education", "Pets",
        "Charity", "Taxes", "Entertainment", "Home Services", "Childcare"
    ]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Convert text to numerical format
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["Description"])
y = df["Category"]

# Train ML Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model and vectorizer
joblib.dump(model, "transaction_classifier.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model trained and saved with a larger dataset!")
