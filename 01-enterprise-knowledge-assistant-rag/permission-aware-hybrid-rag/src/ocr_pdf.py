import shutil
import sys
from pathlib import Path
from typing import cast

import pymupdf as fitz
import pytesseract
from PIL import Image

# Accept a PDF path and optional page limit; default to the bundled large document.
path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/pdfs/large-doc.pdf")
# With no page limit, process the entire document.
max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else None

# pytesseract wraps Tesseract but does not install the executable itself.
if shutil.which("tesseract") is None:
    print(
        "Tesseract is not installed or is not on PATH. Install it on macOS with:\n"
        "  brew install tesseract",
        file=sys.stderr,
    )
    raise SystemExit(1)

with fitz.open(path) as pdf:
    pages_to_read = len(pdf) if max_pages is None else min(max_pages, len(pdf))
    print(
        f"File: {path.name} | Total pages: {len(pdf)} | OCR-ing first {pages_to_read}"
    )

    for i in range(pages_to_read):
        page = pdf[i]

        # 1. Does this page have a real text layer?
        layer_chars = len(cast(str, page.get_text("text")).strip())

        # 2. Render the page to an image and run OCR on it
        pix = page.get_pixmap(dpi=200)
        image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        try:
            text = pytesseract.image_to_string(image).strip()
        except pytesseract.TesseractNotFoundError:
            print(
                "Tesseract could not be started. Install it on macOS with:\n"
                "  brew install tesseract",
                file=sys.stderr,
            )
            raise SystemExit(1) from None

        print(
            f"\n===== PAGE {i + 1} | text-layer characters: {layer_chars} | OCR characters: {len(text)} ====="
        )
        # Print the full result so later table rows are not cut off.
        print(text)
