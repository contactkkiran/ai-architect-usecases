import sys
from pathlib import Path

import pdfplumber

# Use the filename passed on the command line, or default to the sample policy.
filename = sys.argv[1] if len(sys.argv) > 1 else "expense-policy.pdf"
# Sample PDFs are stored in the project's data/pdfs directory.
path = Path("data/pdfs") / filename

# Open the PDF and inspect each page's text and detected tables.
with pdfplumber.open(path) as pdf:
    print("File:", filename, "| Pages:", len(pdf.pages))

    for page_number, page in enumerate(pdf.pages, start=1):
        # Extract and display the page's plain text.
        print(f"\n===== PAGE {page_number}: PLAIN TEXT =====")
        print(page.extract_text())

        # # Extract tables separately because tabular content may not read well as plain text.
        # tables = page.extract_tables()
        # print(f"\n===== PAGE {page_number}: {len(tables)} TABLE(S) =====")
        # for i, table in enumerate(tables, start=1):
        #     print(f"--- Table {i} ---")
        #     for row in table:
        #         print(row)
