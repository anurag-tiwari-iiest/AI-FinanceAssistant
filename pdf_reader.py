import os
import PyPDF2
import re
import streamlit as st
from datetime import datetime

def extract_transactions_from_pdf(pdf_file):
    transactions = []
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text = page.extract_text() or ""
        matches = re.findall(r"(\d{2}-\d{2}-\d{4})\s+(.+?)\s+(\d+\.\d+|\-)\s+(\d+\.\d+|\-)", text)
        for match in matches:
            date_str, particulars, withdrawal, deposit = match
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            date_formatted = date_obj.strftime("%Y-%m-%d")
            if withdrawal != '-':
                amount = -float(withdrawal.replace(',', ''))
            else:
                amount = float(deposit.replace(',', ''))
            transactions.append((date_formatted, particulars.strip(), amount))
    return transactions

def main():
    st.title("PDF Transaction Extractor")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        transactions = extract_transactions_from_pdf(uploaded_file)
        if transactions:
            st.write("Extracted Transactions:")
            for t in transactions:
                st.write(t)
        else:
            st.write("No transactions found in the uploaded PDF.")

if __name__ == "__main__":
    main()
