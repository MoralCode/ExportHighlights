import flet as ft

def main(page: ft.Page):
    def on_file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file_label.value = f"Selected File: {e.files[0].name}"
        else:
            selected_file_label.value = "No file selected."
        selected_file_label.update()

    # Create file picker instance
    file_picker = ft.FilePicker(on_result=on_file_picker_result)

    # Create a label to display the selected file
    selected_file_label = ft.Text("No file selected.")

    # Create a button to open the file picker dialog
    file_button = ft.ElevatedButton(text="Choose File", on_click=lambda _: file_picker.pick_files())

    # Add the file picker to the page
    page.overlay.append(file_picker)

    # Add the button and label to the layout
    page.add(selected_file_label, file_button)

# Run the app
ft.app(target=main)
