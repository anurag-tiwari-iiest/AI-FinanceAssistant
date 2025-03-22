import os
import PyPDF2
import re

def extract_transactions_from_pdf(pdf_path):
    transactions = []
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text() or ""  # Ensures compatibility with newer PyPDF2 versions
            matches = re.findall(r"(\d{4}-\d{2}-\d{2}),(.+),(-?\d+\.\d+)", text)
            for match in matches:
                transactions.append(match)

    return transactions

# Test the function
pdf_path = "sample_statement.pdf"
if not os.path.exists(pdf_path):
    print("⚠ Warning: 'sample_statement.pdf' not found. Ensure the file exists before running this script.")

transactions = extract_transactions_from_pdf(pdf_path)

for t in transactions:
    print(t)  # Format: (Date, Description, Amount)
