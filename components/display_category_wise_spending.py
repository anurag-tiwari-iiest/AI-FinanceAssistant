import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def display_category_wise_spending(df, monthly_spending, budget_df):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("📅 Category-wise Spending for Each Month")

    selected_category = st.selectbox("Select Category", df["Category"].unique(), key="category_select")
    display_months = st.selectbox("Select Duration", [3, 6, 9, 12], key="duration_select")

    col1, col2 = st.columns(2)
    with col1:
        start_year = st.selectbox("Start Year", sorted(df["Date"].dt.year.unique()), key="start_year_select")
    with col2:
        start_month = st.selectbox("Start Month", range(1, 13), key="start_month_select")

    start_period = pd.Period(f"{start_year}-{start_month:02d}", freq="M")
    end_period = start_period + (display_months - 1)

    category_spending = monthly_spending[
        (monthly_spending["Category"] == selected_category) &
        (monthly_spending["Month"] >= start_period) &
        (monthly_spending["Month"] <= end_period)
    ]

    if category_spending.empty:
        st.write(f"No data available for {selected_category} in the selected period.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(category_spending["Month"].astype(str), abs(category_spending["Amount"]))
    for bar, amount in zip(bars, category_spending["Amount"]):
        budget_query = budget_df.loc[
            (budget_df["Month"] == start_period) & (budget_df["Category"] == selected_category), 
            "Budget"
        ]
        budgeted = budget_query.values[0] if not budget_query.empty else 0
        bar.set_color('red' if abs(amount) > budgeted else 'blue')
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"${abs(amount):,.2f}", ha='center', va='bottom')

    ax.axhline(y=budgeted, color='gray', linestyle='--', linewidth=2, label='Budget')

    ax.set_title(f"Spending per Month for {selected_category}")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount ($)")
    ax.legend()
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)