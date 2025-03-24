import os
import PyPDF2
import re
import streamlit as st
from datetime import datetime

def extract_transactions_from_pdf(pdf_file):
    transactions = []
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text = page.extract_text() or ""  # Ensures compatibility with newer PyPDF2 versions

        # Regex to match date, particulars, withdrawals, and deposits
        matches = re.findall(r"(\d{2}-\d{2}-\d{4})\s+(.+?)\s+(\d+\.\d+|\-)\s+(\d+\.\d+|\-)", text)
        
        for match in matches:
            date_str, particulars, withdrawal, deposit = match
            # Convert date to yyyy-mm-dd format
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            date_formatted = date_obj.strftime("%Y-%m-%d")

            # Determine the transaction amount
            if withdrawal != '-':
                amount = -float(withdrawal.replace(',', ''))
            else:
                amount = float(deposit.replace(',', ''))

            transactions.append((date_formatted, particulars.strip(), amount))

    return transactions

# Streamlit app to upload and read PDF
def main():
    st.title("PDF Transaction Extractor")
    
    # File uploader widget
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Extract transactions from the uploaded PDF
        transactions = extract_transactions_from_pdf(uploaded_file)
        
        # Display extracted transactions
        if transactions:
            st.write("Extracted Transactions:")
            for t in transactions:
                st.write(t)  # Format: (Date, Category, Amount)
        else:
            st.write("No transactions found in the uploaded PDF.")
    
if __name__ == "__main__":
    main()
