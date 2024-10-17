import fitz  # PyMuPDF
import argparse
from pathlib import Path
def extract_highlighted_text(pdf_file):
    # Open the PDF
    doc = fitz.open(pdf_file)

    highlights = []

    # Iterate over all pages
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        # Extract annotations (highlights)
        annotations = page.annots()

        if annotations:
            for annot in annotations:
                if annot.info["subtype"] == "Highlight":
                    # Get the highlighted text
                    highlight = page.get_text("highlight", annot)
                    highlights.append(highlight)

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
