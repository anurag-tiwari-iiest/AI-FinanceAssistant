import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def display_spending_vs_budget(monthly_spending, selected_year, selected_month, budget_df):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("📊 Monthly Spending vs Budget")

    categories_to_display = st.multiselect("Select Categories to Display", budget_df["Category"].unique(), default=list(budget_df["Category"].unique()))

    months_option = st.selectbox("Select Duration", ["Last 3 months", "Last 6 months", "Last 1 year", "Custom"])
    if months_option == "Last 3 months":
        display_months = 3
    elif months_option == "Last 6 months":
        display_months = 6
    elif months_option == "Last 1 year":
        display_months = 12
    else:
        display_months = st.number_input("Enter number of months to display", min_value=1, value=3)

    selected_months = pd.date_range(end=pd.to_datetime(f"{selected_year}-{selected_month}"), periods=display_months, freq='M').to_period('M')

    fig, ax = plt.subplots(figsize=(10, 5))

    for category in categories_to_display:
        category_spending = monthly_spending[(monthly_spending["Category"] == category) & (monthly_spending["Month"].isin(selected_months))]
        if category_spending.empty:
            st.write(f"No data available for {category} in the selected months.")
            continue
        ax.plot(category_spending["Month"].astype(str), abs(category_spending["Amount"]), label=f"Spent - {category}")

    for category in categories_to_display:
        budget_query = budget_df.loc[
            (budget_df["Month"].isin(selected_months)) & (budget_df["Category"] == category),
            "Budget"
        ]
        if budget_query.empty:
            st.write(f"No budget data available for {category} in the selected months.")
            continue
        limit = budget_query.values[0]
        category_months = monthly_spending[(monthly_spending["Category"] == category) & (monthly_spending["Month"].isin(selected_months))]["Month"].astype(str)
        ax.plot(category_months, [limit] * len(category_months), "--", label=f"Budget - {category}")

    ax.set_title("Monthly Spending vs Budget")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount ($)")
    ax.legend()
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)