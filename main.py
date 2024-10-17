import fitz  # PyMuPDF
import argparse
from pathlib import Path
def extract_highlighted_text(pdf_file):
    # Open the PDF
    doc = fitz.open(pdf_file)

    highlights = []

    for page in doc:
        for annot in page.annots():
            # https://github.com/pymupdf/PyMuPDF/discussions/1573
            text = page.get_textbox(annot.rect)
            if annot.type[0] == 8:  # 8 corresponds to Highlight annotations
                highlights.append(text)


    return highlights


parser = argparse.ArgumentParser(description="Parse Highlighted sections from Okular highlighted PDF files")
parser.add_argument("pdf_file", help="Path to the Okular highlighted PDF file")
args = parser.parse_args()


pdfPath = Path(args.pdf_file)

if not pdfPath.exists():
    print(f"Error: {pdfPath} does not exist.")
    exit(1)


# Example usage
highlights = extract_highlighted_text(str(pdfPath))

for idx, highlight in enumerate(highlights):
    print(f"Highlight {idx + 1}: {highlight}")
