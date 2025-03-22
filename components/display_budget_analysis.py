import streamlit as st
import pandas as pd

def display_budget_analysis(monthly_spending, selected_period, budget_df):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">Monthly Budget Analysis for {selected_period}</div>', unsafe_allow_html=True)

    month_data = monthly_spending[monthly_spending["Month"] == selected_period]
    if month_data.empty:
        st.write("No data available for the selected period.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    table_data = []

    for _, row in month_data.iterrows():
        category = row["Category"]
        actual_spent = abs(row["Amount"])

        budget_query = budget_df.loc[
            (budget_df["Month"] == selected_period) & (budget_df["Category"] == category), 
            "Budget"
        ]

        budgeted = budget_query.values[0] if not budget_query.empty else 0
        over_budget = max(0, actual_spent - budgeted)
        status = "✅" if over_budget == 0 else "❌"

        table_data.append([
            category, 
            f"${budgeted:.2f}", 
            f"${actual_spent:.2f}", 
            f"${over_budget:.2f}", 
            status
        ])

    table_df = pd.DataFrame(table_data, columns=["Category", "Budget ($)", "Spent ($)", "Over Budget ($)", "Status"])
    st.table(table_df)
    st.markdown('</div>', unsafe_allow_html=True)