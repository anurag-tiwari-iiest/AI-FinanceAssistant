import streamlit as st

def display_income_and_spending(monthly_income, monthly_spending, selected_period):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">💰 Total Monthly Income</div>', unsafe_allow_html=True)
        income_data = monthly_income[monthly_income["Month"] == selected_period]
        income_amount = income_data['Amount'].values[0] if not income_data.empty else 0
        st.markdown(f"""
            <div style="font-size: 1.5rem; font-weight: bold; color: #1e88e5;">${income_amount:,.2f}</div>
            <div style="font-size: 1rem; color: #555;">Income for {selected_period}</div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">💸 Total Monthly Spending</div>', unsafe_allow_html=True)
        spending_data = monthly_spending[monthly_spending["Month"] == selected_period]
        total_spending = abs(spending_data["Amount"].sum()) if not spending_data.empty else 0
        st.markdown(f"""
            <div style="font-size: 1.5rem; font-weight: bold; color: #d32f2f;">${total_spending:,.2f}</div>
            <div style="font-size: 1rem; color: #555;">Spending for {selected_period}</div>
        """, unsafe_allow_html=True)

    savings = income_amount - total_spending
    percent_spent = (total_spending / income_amount) * 100 if income_amount > 0 else 0

    if savings >= 0:
        savings_label = "💰 Total Savings:"
        savings_color = "#43a047"
    else:
        savings_label = "⚠️ Deficit:"
        savings_color = "#d32f2f"

    st.markdown(f"""
        <div style="font-size: 1.2rem; margin-top: 1rem;">
            📊 <b>{percent_spent:.2f}%</b> of your income spent
        </div>
        <div style="font-size: 1.2rem; color: {savings_color}; margin-top: 0.5rem;">
            {savings_label} <b>${abs(savings):,.2f}</b>
        </div>
    """, unsafe_allow_html=True)