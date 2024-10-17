import fitz  # PyMuPDF
import argparse
from pathlib import Path
def extract_highlighted_text(pdf_file):
    # Open the PDF
    doc = fitz.open(pdf_file)

    annotations = []

    for page in doc:
        for annot in page.annots():

            annotation = {}
            
            # if annot.type[0] == 8:  # 8 corresponds to Highlight annotations
            annotation['type'] = {
                "name": annot.type[1],
                "code": annot.type[0]
            }
            annotation['color'] = annot.colors
            annotation['location'] = annot.rect  # in page coordinates (x0, y0, x1, y1)
            # https://github.com/pymupdf/PyMuPDF/discussions/1573
            annotation['selected_text'] = page.get_textbox(annot.rect)
            annotation['additional_text'] = annot.get_text()

            annotations.append(annotation)

    return annotations

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse Highlighted sections from Okular highlighted PDF files")
    parser.add_argument("pdf_file", help="Path to the Okular highlighted PDF file")
    args = parser.parse_args()


    pdfPath = Path(args.pdf_file)

    if not pdfPath.exists():
        print(f"Error: {pdfPath} does not exist.")
        exit(1)


    # Example usage
    highlights = extract_highlighted_text(str(pdfPath))

    print(len(highlights))
    for idx, highlight in enumerate(highlights):
        print(f"Highlight {idx + 1}: {highlight}")
