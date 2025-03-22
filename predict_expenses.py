import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def run_expense_prediction():
    # Verify that the required file exists
    file_path = "categorized_transactions.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError("❌ Error: 'categorized_transactions.csv' not found! Run 'categorize_expenses.py' first.")

    # Load transactions
    df = pd.read_csv(file_path)

    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    # Aggregate expenses by month
    monthly_expenses = df[df["Amount"] < 0].groupby(pd.Grouper(freq="M"))["Amount"].sum().abs().to_frame()
    monthly_expenses.rename(columns={"Amount": "Expense"}, inplace=True)

    # Ensure there is enough data
    if len(monthly_expenses) < 12:
        raise ValueError("❌ Error: Not enough data for ML forecasting. At least 12 months of data required.")

    # Create lag features (past values as features)
    for i in range(1, 4):  # Use past 3 months as features
        monthly_expenses[f"lag_{i}"] = monthly_expenses["Expense"].shift(i)

    # Drop rows with NaN values (first 3 months will be NaN due to shifting)
    monthly_expenses.dropna(inplace=True)

    # Split into training & testing data
    train_data = monthly_expenses[:-3]  # Use all but last 3 months for training
    test_data = monthly_expenses[-3:]   # Last 3 months for testing

    X_train, y_train = train_data.drop(columns=["Expense"]), train_data["Expense"]
    X_test, y_test = test_data.drop(columns=["Expense"]), test_data["Expense"]

    # Train XGBoost model
    model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1)
    model.fit(X_train, y_train)

    # Predict next 3 months
    predictions = model.predict(X_test)

    # Evaluate model
    mae = mean_absolute_error(y_test, predictions)
    print(f"📊 Model MAE: {mae:.2f}")

    # Forecast next 3 months
    future_dates = pd.date_range(start=monthly_expenses.index[-1] + pd.DateOffset(months=1), periods=3, freq='M')
    future_expenses = pd.DataFrame(index=future_dates, columns=["Expense"])

    # Use the last available data for prediction
    last_known = monthly_expenses.iloc[-1].drop("Expense")

    for i in range(3):
        pred = model.predict(np.array(last_known).reshape(1, -1))[0]  # Predict
        future_expenses.iloc[i] = pred  # Store prediction
        last_known = last_known.shift(1)  # Shift values to simulate new month
        last_known.iloc[0] = pred  # Replace first lag with the new prediction

    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_expenses.index[-12:], monthly_expenses["Expense"][-12:], label="Past Expenses", marker='o')
    plt.plot(future_expenses.index, future_expenses["Expense"], label="Predicted Expenses", linestyle="dashed", marker='x')

    plt.legend()
    plt.title("ML-Based Expense Forecast")
    plt.xlabel("Date")
    plt.ylabel("Amount ($)")
    plt.grid(True)
    
    fig = plt.gcf()
    plt.close(fig)
    
    # Combine past 3 months and next 3 months expenses for the table
    combined_expenses = pd.concat([monthly_expenses[["Expense"]][-3:], future_expenses], axis=0)

    # Format dates as MM-YYYY
    combined_expenses.index = combined_expenses.index.strftime('%m-%Y')

    return fig, combined_expenses