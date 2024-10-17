import flet as ft
import os
from pathlib import Path
from main import extract_highlighted_text, PdfAnnotationType
from helpers import split_dict_list

def merge_highlights(highlights, micro_combine=" ", macro_combine="\n\n" ):
    """ merge a grouped set of highlights into a list of strings of their contents
    """

    #check if all items in highlights are dictionaries and if so combine them.

    # base case: all are highlights
    if all(isinstance(highlight, dict) for highlight in highlights):
        return micro_combine.join([x["selected_text"] for x in highlights])

    # base case: all are strings (already merged)
    if all(isinstance(highlight, str) for highlight in highlights):
        return macro_combine.join(highlights)

    # recursive case: mix of types (highlight, string, list)
    return macro_combine.join([merge_highlights(h, micro_combine, macro_combine) for h in highlights])


def group_highlights(highlights, tolerance=10):
    """ evaluate every pair of highlights and create a final combined list of them
    """
    highlights = list(highlights)

    sortkey = lambda f: f["location"]["top"] + (f["location"]["left"] / 10)

    combined_highlights = []


    by_page = split_dict_list(highlights, lambda x: x["page_number"], sortkey)

    for page_sublist in by_page:

        by_start_line = split_dict_list(page_sublist, lambda f: f["location"]["top"], sortkey)

        combined_highlights.append(by_start_line)
    
    return combined_highlights
    

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

                highlights = group_highlights(highlights)
                merged = merge_highlights(highlights)
                
                # Display extracted highlights in the UI
                highlight_text.value = merged
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
