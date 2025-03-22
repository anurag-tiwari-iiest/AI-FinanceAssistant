import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def display_category_comparison(df, expenses_df, budget_df):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("📊 Category-wise Spending Comparison")

    col1, col2 = st.columns(2)
    with col1:
        start_year = st.selectbox("Start Year", sorted(df["Date"].dt.year.unique()), key="start_year_comparison")
    with col2:
        start_month = st.selectbox("Start Month", range(1, 13), key="start_month_comparison")
    
    start_period = pd.Period(f"{start_year}-{start_month:02d}", freq="M")
    
    with col1:
        end_year = st.selectbox("End Year", sorted(df["Date"].dt.year.unique()), key="end_year_comparison")
    with col2:
        end_month = st.selectbox("End Month", range(1, 13), key="end_month_comparison")

    end_period = pd.Period(f"{end_year}-{end_month:02d}", freq="M")

    category_total_spending = expenses_df[(expenses_df["Month"] >= start_period) & (expenses_df["Month"] <= end_period)].groupby("Category")["Amount"].sum()

    if category_total_spending.empty:
        st.write("No data available for the selected period.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['red' if (
        not budget_df.loc[
            (budget_df["Month"] == start_period) & (budget_df["Category"] == cat), 
            "Budget"
        ].empty and abs(category_total_spending[cat]) > budget_df.loc[
            (budget_df["Month"] == start_period) & (budget_df["Category"] == cat), 
            "Budget"
        ].values[0]
    ) else 'blue' for cat in category_total_spending.index]
    bars = ax.bar(category_total_spending.index, category_total_spending.abs(), color=colors)
    ax.set_title("Total Spending per Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Spending")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    st.subheader("Category-wise Spending Table")
    table_data = []
    for category, amount in category_total_spending.items():
        actual_spent = abs(amount)
        budget_query = budget_df.loc[
            (budget_df["Month"] == start_period) & (budget_df["Category"] == category), 
            "Budget"
        ]
        budgeted = budget_query.values[0] if not budget_query.empty else 0
        over_budget = max(0, actual_spent - budgeted)
        status = "✅" if over_budget == 0 else "❌"
        table_data.append([category, budgeted, actual_spent, over_budget, status])

    table_df = pd.DataFrame(table_data, columns=["Category", "Budget ($)", "Spent ($)", "Over Budget ($)", "Status"])
    st.table(table_df)
    st.markdown('</div>', unsafe_allow_html=True)