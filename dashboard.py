import os
import streamlit as st
import pandas as pd
import datetime
import predict_expenses

# Importing the components
from components.display_income_and_spending import display_income_and_spending
from components.display_budget_analysis import display_budget_analysis
from components.display_spending_vs_budget import display_spending_vs_budget
from components.compare_spending_between_months import compare_spending_between_months
from components.display_category_wise_spending import display_category_wise_spending
from components.display_spending_trends import display_spending_trends
from components.display_category_comparison import display_category_comparison

st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="💸",
    layout="wide"
)

# Custom CSS for styling and themes
st.markdown("""
    <style>
    .main-container {
        padding: 2rem;
        border: 1px solid var(--primary-color);
        border-radius: 10px;
        background-color: var(--secondary-color);
        margin-bottom: 2rem;
        color: var(--text-color);
    }

    .section-header {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: var(--primary-color);
    }

    .subsection-header {
        font-size: 1.2rem;
        margin-bottom: 1rem;
        color: var(--primary-color);
    }

    .footer {
        text-align: center;
        padding: 1rem;
        border-top: 1px solid var(--primary-color);
        margin-top: 2rem;
        color: var(--primary-color);
    }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    df = pd.read_csv("categorized_transactions.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()
df["Category"] = df["Category"].replace("Transport", "Auto & Transport")

income_categories = ["Salary", "Income"]
expenses_df = df[~df["Category"].isin(income_categories)]
income_df = df[df["Category"].isin(income_categories)]
df_grouped = expenses_df.groupby("Category")["Amount"].sum()

# Group expenses by Month & Category
expenses_df["Month"] = expenses_df["Date"].dt.to_period("M")
monthly_spending = expenses_df.groupby(["Month", "Category"])["Amount"].sum().reset_index()

# Group income by Month
income_df["Month"] = income_df["Date"].dt.to_period("M")
monthly_income = income_df.groupby("Month")["Amount"].sum().reset_index()

budget_file = "budgets.csv"

# Check if the budget file exists; if not, create it with default values
if not os.path.exists(budget_file):
    categories = expenses_df["Category"].unique()
    months = pd.date_range("2024-01-01", "2025-12-31", freq="MS").to_period("M")
    budget_df = pd.DataFrame([
        {"Month": month, "Category": category, "Budget": 500}
        for month in months for category in categories
    ])
    budget_df.to_csv(budget_file, index=False)
else:
    budget_df = pd.read_csv(budget_file)
    budget_df["Month"] = pd.to_datetime(budget_df["Month"]).dt.to_period("M")

# Sidebar: Month and Year Selection
st.sidebar.header("Select Month and Year")
current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month

years = list(range(2020, 2031))
months = range(1, 13)

col1, col2 = st.sidebar.columns(2)
with col1:
    selected_year = st.selectbox("Year", years, index=years.index(current_year), key="year_select")
with col2:
    selected_month = st.selectbox("Month", months, index=current_month - 1, key="month_select")

selected_period = pd.Period(f"{selected_year}-{selected_month:02d}", freq="M")

# Sidebar: Navigation
st.sidebar.header("Navigation")
pages = ["Overview", "Spending vs Budget", "Compare Spending", "Category-wise Spending", "Spending Trends", "Category Comparison", "Predict Expenses", "Suggestions"]
selected_page = st.sidebar.radio("Go to", pages)

# Sidebar: User Budget Input (Per Month and Category)
st.sidebar.header("Set Monthly Budgets")

# Separate Year and Month selection for budget setting
col1, col2 = st.sidebar.columns(2)
with col1:
    budget_year = st.selectbox("Budget Year", years, index=years.index(current_year), key="budget_year_select")
with col2:
    budget_month = st.selectbox("Budget Month", months, index=current_month - 1, key="budget_month_select")

selected_budget_period = pd.Period(f"{budget_year}-{budget_month:02d}", freq="M")
selected_category = st.sidebar.selectbox("Select Category", budget_df["Category"].unique())

# Retrieve the current budget for the selected month and category
budget_query = budget_df.loc[
    (budget_df["Month"] == selected_budget_period) & (budget_df["Category"] == selected_category), 
    "Budget"
]

# Show the current budget if it exists, otherwise default to 500
current_budget = int(budget_query.values[0]) if not budget_query.empty else 500

# Input to update the budget
new_budget = st.sidebar.number_input(
    f"Set Budget for {selected_category} in {selected_budget_period}",
    min_value=0,
    max_value=20000,
    value=current_budget,
    step=100
)

# Update the budget DataFrame with the new value
if budget_query.empty:
    new_row = pd.DataFrame({"Month": [selected_budget_period], "Category": [selected_category], "Budget": [new_budget]})
    budget_df = pd.concat([budget_df, new_row], ignore_index=True)
else:
    budget_df.loc[
        (budget_df["Month"] == selected_budget_period) & (budget_df["Category"] == selected_category), 
        "Budget"
    ] = new_budget

# Save the updated budget DataFrame to the CSV file
budget_df.to_csv(budget_file, index=False)

# Function to display footer
def display_footer():
    st.markdown("<br><hr><p class='footer'>🚀 Finance Dashboard by Anurag</p>", unsafe_allow_html=True)

def saving_recommendations(df_grouped, budget_df, selected_period):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("💡 Savings Recommendations")

    total_savings = 0
    savings_goals = []
    alternative_options = []

    # Calculate total savings and identify savings goals
    total_income = income_df[income_df["Month"] == selected_period]["Amount"].sum()
    if total_income > 0:
        suggested_savings = total_income * 0.20  # Suggest saving 20% of income
        savings_goals.append(f"🏦 Consider setting aside ${suggested_savings:.2f} as savings this month.")

    # Suggest alternatives for high-cost items or services
    alternative_options.append("🚗 Consider carpooling, public transport, or biking to save on transport costs.")
    alternative_options.append("🍽️ Consider home-cooking or meal-prepping to reduce dining out expenses.")
    alternative_options.append("🛍️ Look for sales, discounts, or consider second-hand options to save on shopping.")

    # Display savings goals
    for goal in savings_goals:
        st.write(goal)

    # Display alternative options
    for option in alternative_options:
        st.write(option)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Function to check budget exceedance
def check_budget_exceedance(df_grouped, budget_df, selected_period):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("Budget Analysis")

    # Create a DataFrame to store budget exceedance information
    exceedance_data = []

    for category, amount in df_grouped.items():
        budget_query = budget_df.loc[
            (budget_df["Month"] == selected_period) & (budget_df["Category"] == category), 
            "Budget"
        ]
        if not budget_query.empty and abs(amount) > budget_query.values[0]:
            exceedance_data.append({
                "Category": category,
                "Overbudget Value": abs(amount) - budget_query.values[0]
            })

    if exceedance_data:
        exceedance_df = pd.DataFrame(exceedance_data)
        st.table(exceedance_df)
    else:
        st.info("No budget exceedance for the selected period.")

    st.markdown('</div>', unsafe_allow_html=True)

# Function to display suspicious transactions
def display_suspicious_transactions(df, selected_period):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("Suspicious Transactions")

    # Load suspicious transactions
    if os.path.exists("fraud_transactions.csv"):
        fraud_df = pd.read_csv("fraud_transactions.csv")
        fraud_df["Date"] = pd.to_datetime(fraud_df["Date"]).dt.strftime('%Y-%m-%d')
        fraud_df["Month"] = pd.to_datetime(fraud_df["Date"]).dt.to_period("M")
        fraud_df = fraud_df[fraud_df["Month"] == selected_period]

        if not fraud_df.empty:
            fraud_df["Model Check"] = fraud_df["Model_Fraud_Flag"].apply(lambda x: '❌' if x == -1 else '✔️')
            fraud_df["Large Amount Check"] = fraud_df["Large_Amount_Flag"].apply(lambda x: '❌' if x == 1 else '✔️')
            fraud_df["Odd Hour Check"] = fraud_df["Odd_Hour_Flag"].apply(lambda x: '❌' if x == 1 else '✔️')
            fraud_df["Final Check"] = fraud_df["Final_Fraud"].apply(lambda x: '❌' if x == 1 else '✔️')

            # Format Amount column
            fraud_df["Amount"] = fraud_df["Amount"].apply(lambda x: f'{abs(x):,.0f}')

            # Adjust column widths for better readability
            fraud_df = fraud_df.rename(columns={"Description": "Description"})
            
            st.table(fraud_df[["Date", "Description", "Amount", "Model Check", "Large Amount Check", "Odd Hour Check", "Final Check"]])
        else:
            st.info("No suspicious transactions found for the selected period.")
    else:
        st.info("No suspicious transactions found.")

    st.markdown('</div>', unsafe_allow_html=True)

# Render the selected page
if selected_page == "Overview":
    display_income_and_spending(monthly_income, monthly_spending, selected_period)
    display_budget_analysis(monthly_spending, selected_period, budget_df)
elif selected_page == "Spending vs Budget":
    display_spending_vs_budget(monthly_spending, selected_year, selected_month, budget_df)
elif selected_page == "Compare Spending":
    compare_spending_between_months(expenses_df, monthly_spending)
elif selected_page == "Category-wise Spending":
    display_category_wise_spending(df, monthly_spending, budget_df)
elif selected_page == "Spending Trends":
    display_spending_trends(expenses_df)
elif selected_page == "Category Comparison":
    display_category_comparison(df, expenses_df, budget_df)
elif selected_page == "Predict Expenses":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("🔮 Expense Predictions")
    fig, combined_expenses = predict_expenses.run_expense_prediction()
    st.pyplot(fig)
    st.subheader("📊 Expense Data")
    st.table(combined_expenses)
    st.markdown('</div>', unsafe_allow_html=True)
elif selected_page == "Suggestions":
    saving_recommendations(df_grouped, budget_df, selected_period)
    check_budget_exceedance(df_grouped, budget_df, selected_period)
    display_suspicious_transactions(df, selected_period)

display_footer()