import flet as ft
import os
import tempfile
import atexit
from tnefparse import TNEF
from flet import FilePicker, FilePickerResultEvent
import subprocess
import platform

# Global list to keep track of temporary files
temp_files = []

def cleanup_temp_files():
    global temp_files
    for file_path in temp_files:
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception:
            pass  # Ignore errors during cleanup
    temp_files = []

# Register the cleanup function to run at exit
atexit.register(cleanup_temp_files)

def main(page: ft.Page):
    page.title = "Winmail.dat Decryptor"
    decrypted_files = []

    def pick_file(e: FilePickerResultEvent):
        if e.files:
            winmail_file.value = e.files[0].path
            decrypt_file(e)
            page.update()

    def decrypt_file(e):
        file_path = winmail_file.value
        if file_path and os.path.exists(file_path):
            decrypted_files.clear()
            with open(file_path, 'rb') as f:
                file_data = f.read()
                tnef = TNEF(file_data)
                for attachment in tnef.attachments:
                    decrypted_files.append((attachment.name, attachment.data))
            
            decrypted_list.controls.clear()
            for filename, _ in decrypted_files:
                file_item = ft.TextButton(filename, on_click=lambda e, name=filename: open_file(name))
                decrypted_list.controls.append(file_item)
            page.update()

    def save_files(e: FilePickerResultEvent):
        if e.path and decrypted_files:
            for filename, data in decrypted_files:
                save_path = os.path.join(e.path, filename)
                with open(save_path, 'wb') as output_file:
                    output_file.write(data)
            page.snack_bar = ft.SnackBar(ft.Text("Files saved successfully!"))
            page.snack_bar.open = True
            page.update()

    def open_file(filename):
        for name, data in decrypted_files:
            if name == filename:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(name)[1]) as temp_file:
                    temp_file.write(data)
                    temp_file_path = temp_file.name
                try:
                    if platform.system() == "Windows":
                        os.startfile(temp_file_path)
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.call(('open', temp_file_path))
                    else:  # Linux and Android
                        subprocess.call(('xdg-open', temp_file_path))
                    
                    # Add the temp file to the global list for later cleanup
                    global temp_files
                    temp_files.append(temp_file_path)
                except Exception as e:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Error opening file: {str(e)}"))
                    page.snack_bar.open = True
                    page.update()
                break

    winmail_file = ft.TextField(label="Selected File", disabled=True)
    pick_button = ft.ElevatedButton("Pick winmail.dat", on_click=lambda _: file_picker.pick_files())
    save_button = ft.ElevatedButton("Save Files", on_click=lambda _: save_picker.get_directory_path())
    
    decrypted_list = ft.Column()
    file_picker = FilePicker(on_result=pick_file)
    save_picker = FilePicker(on_result=save_files)
    page.overlay.extend([file_picker, save_picker])

    page.add(
        winmail_file,
        pick_button,
        decrypted_list,
        save_button
    )

ft.app(target=main)
