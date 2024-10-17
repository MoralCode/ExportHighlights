import fitz  # PyMuPDF

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


# Example usage
pdf_file = "path/to/your/file.pdf"
highlights = extract_highlighted_text(pdf_file)

for idx, highlight in enumerate(highlights):
    print(f"Highlight {idx + 1}: {highlight}")
