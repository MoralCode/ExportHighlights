import flet as ft
import os
from pathlib import Path
from main import extract_highlighted_text

def main(page: ft.Page):
    def on_file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:

            for f in e.files:
                filepath = Path(f.path)
                if len(e.files) > 1:
                    selected_file_label.value = f"Selected Multiple Files: {filepath.basename()}"

                else:
                    selected_file_label.value = f"Selected File: {os.path.basename(filepath)}"
            
                # Process the selected PDF and extract highlights
                highlights = extract_highlighted_text(filepath)
                
                # Display extracted highlights in the UI
                highlight_text.value = "\n".join(highlights)
        else:
            selected_file_label.value = "No file selected."
            highlight_text.value = ""

        # Update UI elements
        selected_file_label.update()
        highlight_text.update()

    # Create file picker instance
    file_picker = ft.FilePicker(on_result=on_file_picker_result)

    # Create a label to display the selected file
    selected_file_label = ft.Text("No file selected.")

    # Create a button to open the file picker dialog
    file_button = ft.ElevatedButton(text="Choose PDF File", on_click=lambda _: file_picker.pick_files(allowed_extensions=["pdf"]))

    # Text area to display extracted highlights
    highlight_text = ft.TextField(
        label="Extracted Highlights:",
        multiline=True,
        min_lines=1,
        max_lines=100,
        border=ft.InputBorder.NONE,
    )

    # Add the file picker to the page
    page.overlay.append(file_picker)

    # Add components to the page layout
    page.add(
        selected_file_label,
        file_button,
        highlight_text
    )

# Run the app
ft.app(target=main)
