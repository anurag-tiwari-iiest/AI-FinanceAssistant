import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def display_spending_trends(expenses_df):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("📈 Monthly Spending Trends")
    monthly_total_spending = expenses_df.groupby(pd.Grouper(key="Date", freq="ME"))["Amount"].sum()

    if monthly_total_spending.empty:
        st.write("No data available for the selected period.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_total_spending.index, monthly_total_spending.abs(), marker="o", linestyle="-")
    ax.set_title("Spending Over Time")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Spending")
    ax.axhline(monthly_total_spending.abs().mean(), color='blue', linestyle='--', label='Average Spending')
    ax.legend()
    plt.xticks(rotation=60)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)