import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def compare_spending_between_months(expenses_df, monthly_spending):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("📉 Compare Spending Between Months")

    col1, col2 = st.columns(2)
    with col1:
        start_year = st.selectbox("Start Year", sorted(expenses_df["Date"].dt.year.unique()), key="start_year_compare")
    with col2:
        start_month = st.selectbox("Start Month", range(1, 13), key="start_month_compare")

    col1, col2 = st.columns(2)
    with col1:
        end_year = st.selectbox("End Year", sorted(expenses_df["Date"].dt.year.unique()), key="end_year_compare")
    with col2:
        end_month = st.selectbox("End Month", range(1, 13), key="end_month_compare")

    start_period = pd.Period(f"{start_year}-{start_month:02d}", freq="M")
    end_period = pd.Period(f"{end_year}-{end_month:02d}", freq="M")

    comparison_data = monthly_spending[(monthly_spending["Month"] >= start_period) & (monthly_spending["Month"] <= end_period)]
    if comparison_data.empty:
        st.write("No data available for the selected period.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    comparison_pivot = comparison_data.pivot(index="Category", columns="Month", values="Amount").fillna(0)
    comparison_pivot.loc["Total"] = comparison_pivot.sum(axis=0)
    st.dataframe(comparison_pivot)

    fig, ax = plt.subplots(figsize=(10, 5))
    comparison_pivot.T.plot(kind="bar", stacked=True, ax=ax)
    plt.title("Spending Comparison Between Selected Months")
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)