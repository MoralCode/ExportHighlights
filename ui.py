import flet as ft
import os
from pathlib import Path
from main import extract_highlighted_text, PdfAnnotationType

def combine_highlight_pair(highlight_a, highlight_b, tolerance=10):
    """ attempt to combine a pair  of highlights based on certain 
    criteria (e.g. keeping highlights on the same line if they started there)

    Arguments:
    highlights -- list of dictionaries representing highlights to combine
    tolerance -- tolerance distance for considering two values "the same"

    Returns:
        A list of two highlights if they could not be combined
        A list of a list of highlights if they could be combined
    """


    # detect if the highlights both start on the same line (y coordinate)
    if highlight_a.location.top - highlight_b.location.top < tolerance:
        return [[ highlight_a, highlight_b ]]
    
    return [ highlight_a, highlight_b ]
def main(page: ft.Page):
    def on_file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            if len(e.files) > 1:
                selected_file_label.value = f"Selected {len(e.files)} Files:"
            else:
                selected_file_label.value = f"Selected File:  {e.files[0].path}"

            for f in e.files:
                filepath = Path(f.path)

                # Text area to display extracted highlights
                highlight_text = ft.TextField(
                    label=f"Extracted Highlights from {filepath.name}:",
                    multiline=True,
                    min_lines=1,
                    max_lines=100,
                    border=ft.InputBorder.NONE,
                )
            
                # Process the selected PDF and extract highlights
                highlights = extract_highlighted_text(filepath, type_filter=PdfAnnotationType.Highlight)

                highlights = map(lambda x: x['selected_text'], highlights)
                
                # Display extracted highlights in the UI
                highlight_text.value = "\n\n".join(highlights)
                highlightFilesList.controls.append(highlight_text)

        else:
            selected_file_label.value = "No file selected."
            

        # Update UI elements
        selected_file_label.update()
        highlightFilesList.update()

    # Create file picker instance
    file_picker = ft.FilePicker(on_result=on_file_picker_result)

    # Create a label to display the selected file
    selected_file_label = ft.Text("No file selected.")

    # Create a button to open the file picker dialog
    file_button = ft.ElevatedButton(text="Choose PDF File", on_click=lambda _: file_picker.pick_files(allowed_extensions=["pdf"], allow_multiple=True))


    highlightFilesList = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    # Add the file picker to the page
    page.overlay.append(file_picker)

    # Add components to the page layout
    page.add(
        selected_file_label,
        file_button,
        highlightFilesList
    )

# Run the app
ft.app(target=main)
