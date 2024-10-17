import fitz  # PyMuPDF
import argparse
from pathlib import Path
from enum import Enum

class PdfAnnotationType(Enum):
    Text = 0
    FreeText = 2
    Highlight = 8
    Underline = 9
    Squiggly = 10
    StrikeOut = 11
    Redact = 12
    Stamp = 13
    Caret = 14
    Popup = 16


def rect_to_ltrb(rect, as_dict=True):
    # Rect.x0 - left corners’ x coordinate
    # Rect.x1 - right corners’ x -coordinate
    # Rect.y0 - top corners’ y coordinate
    # Rect.y1 - bottom corners’ y coordinate
    if as_dict:
        return {"left": rect.x0, "top": rect.y0, "right": rect.x1, "bottom": rect.y1}
    else:  # return as a tuple of (left, top, right, bottom) coordinates
        return (rect.x0, rect.y0, rect.x1, rect.y1)

def extract_highlighted_text(pdf_file, type_filter:PdfAnnotationType=None):
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
            annotation['page_number'] = page.number
            annotation['color'] = annot.colors
            annotation['location'] = rect_to_ltrb(annot.rect)  # in page coordinates (x0, y0, x1, y1)
            # https://github.com/pymupdf/PyMuPDF/discussions/1573
            annotation['selected_text'] = page.get_textbox(annot.rect)
            annotation['additional_text'] = annot.get_text()

            if type_filter is not None and annot.type[0]!= type_filter.value:
                continue

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
