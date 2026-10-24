import sys
from pathlib import Path

import pdfplumber

HEADER_HEIGHT = 50  # points cropped from the top (running header)
FOOTER_HEIGHT = 40  # points cropped from the bottom (running footer)


def clean(cell):
    """Collapse line breaks and extra spaces inside a table cell."""
    return " ".join((cell or "").split())


def table_to_sentences(rows):
    """Turn each table row into one line where every value carries its column label."""
    # pdfplumber returns the first row as column headings and the remaining rows as data.
    headers = [clean(c) for c in rows[0]]
    lines = []
    for row in rows[1:]:
        cells = [clean(c) for c in row]
        # Label each cell so a row remains meaningful when used outside the original table.
        pairs = [f"{h} = {v}" for h, v in zip(headers, cells)]
        lines.append("; ".join(pairs) + ".")
    return lines


def add_text(elements, body, top, bottom, page_number):
    """Extract text from the region between two y-positions."""
    # Keep the requested vertical range inside the already-cropped page body.
    top = max(top, body.bbox[1])
    bottom = min(bottom, body.bbox[3])
    # Ignore tiny regions, which are unlikely to contain readable text.
    if bottom - top < 5:
        return
    region = body.crop((0, top, body.width, bottom))
    text = region.extract_text()
    if text and text.strip():
        # Store text blocks in the same result list as tables, with source-page metadata.
        elements.append({"type": "text", "page": page_number, "content": text.strip()})


def parse_pdf(path):
    # Build one ordered list containing each page's text and table content.
    elements = []
    with pdfplumber.open(path) as pdf:
        # Start numbering at 1 to match the page numbers shown in PDF viewers.
        for page_number, page in enumerate(pdf.pages, start=1):
            # Remove repeated headers and footers before extracting the useful page content.
            body = page.crop(
                (0, HEADER_HEIGHT, page.width, page.height - FOOTER_HEIGHT)
            )

            # Locate tables and sort by their top coordinate to preserve reading order.
            tables = sorted(body.find_tables(), key=lambda t: t.bbox[1])

            # Track the top edge of the next text section that has not been processed yet.
            cursor = body.bbox[1]
            for table in tables:
                # Extract the text between the previous boundary and this table.
                add_text(elements, body, cursor, table.bbox[1], page_number)

                # Convert the table rows to labeled sentences, then store them as one block.
                sentences = table_to_sentences(table.extract())
                elements.append(
                    {
                        "type": "table",
                        "page": page_number,
                        "content": "\n".join(sentences),
                    }
                )

                # Continue below this table, preventing its area from being processed as text.
                cursor = table.bbox[3]

            # Capture the final text section; if the page had no tables, this captures the page body.
            add_text(elements, body, cursor, body.bbox[3], page_number)

    # The context manager has closed the PDF; return all extracted blocks to the caller.
    return elements


if __name__ == "__main__":
    # Use the first command-line argument as the PDF name, or default to the sample expense policy.
    filename = sys.argv[1] if len(sys.argv) > 1 else "large-doc.pdf"

    # Resolve the chosen file inside data/pdfs and run the page-by-page extraction flow above.
    elements = parse_pdf(Path("data/pdfs") / filename)

    # Print a summary first so the user can see how many blocks were extracted.
    print(f"File: {filename} | Elements: {len(elements)}")

    # Display each block with its sequence number, content type, and original PDF page number.
    for i, el in enumerate(elements, start=1):
        print(f"\n--- Element {i}: {el['type'].upper()} (page {el['page']}) ---")
        # Print the extracted text or the newline-separated table rows for this block.
        print(el["content"])
