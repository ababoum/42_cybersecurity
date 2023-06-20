#!/usr/bin/env python3

import tkinter as tk
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import sys
import os
import copy


interface = False

arguments = copy.deepcopy(sys.argv[1:])
if len(arguments) >= 1 and arguments[0] == '-i':
    interface = True
    arguments.pop(0)

if len(arguments) == 0 and not interface:
    print('Usage: ./scorpion.py [-i] FILE1 [FILE2 ...]')
    exit()

for arg in arguments:
    print('-' * 80)
    print(f'File: {arg}')
    print('-' * 20)

    # if sys.platform == 'linux':
    #     dt_c = datetime.fromtimestamp(
    #         os.stat(arg).st_birthtime).strftime('%Y-%m-%d %H:%M:%S')
    # else:

    dt_c = datetime.fromtimestamp(
        os.path.getctime(arg)).strftime('%Y-%m-%d %H:%M:%S')

    print(f'Creation date: {dt_c}')
    dt_m = datetime.fromtimestamp(
        os.path.getmtime(arg)).strftime('%Y-%m-%d %H:%M:%S')
    print(f'Modification date: {dt_m}')

    ### EXIF DATA ###

    img = Image.open(arg)
    exif_data = img.getexif()

    print('-' * 20)
    print('EXIF data:')
    print('-' * 20)

    if exif_data:
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            print(f"{tag_name}: {value}")
    else:
        print('No EXIF data.')


#### INTERFACE ####

class MetadataEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Metadata Editor")
        self.geometry("400x300")

        self.file_path = tk.StringVar()
        self.exif_data = {}

        file_label = tk.Label(self, text="Image File:")
        file_label.pack()
        self.file_entry = tk.Entry(self, textvariable=self.file_path)
        self.file_entry.pack()

        load_button = tk.Button(self, text="Load Image",
                                command=self.load_image)
        load_button.pack()

        metadata_label = tk.Label(self, text="Metadata:")
        metadata_label.pack()
        self.metadata_listbox = tk.Listbox(self)
        self.metadata_listbox.pack()

        modify_button = tk.Button(
            self, text="Modify Metadata", command=self.modify_metadata)
        modify_button.pack()

        delete_button = tk.Button(
            self, text="Delete Metadata", command=self.delete_metadata)
        delete_button.pack()

    def load_image(self):
        image_path = self.file_path.get()
        try:
            image = Image.open(image_path)
            self.exif_data = image._getexif() or {}
            self.update_metadata_listbox()
        except IOError as e:
            self.show_error_dialog(f"Error loading image: {e}")

    def update_metadata_listbox(self):
        self.metadata_listbox.delete(0, tk.END)
        for tag_id, value in self.exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            self.metadata_listbox.insert(tk.END, f"{tag_name}: {value}")

    def modify_metadata(self):
        selection = self.metadata_listbox.curselection()
        if selection:
            tag_id = list(self.exif_data.keys())[selection[0]]
            new_value = self.ask_for_user_input("Enter new value:")
            self.exif_data[tag_id] = new_value
            self.update_metadata_listbox()

    def delete_metadata(self):
        selection = self.metadata_listbox.curselection()
        if selection:
            tag_id = list(self.exif_data.keys())[selection[0]]
            del self.exif_data[tag_id]
            self.update_metadata_listbox()

    def ask_for_user_input(self, prompt):
        dialog = UserInputDialog(self, prompt)
        self.wait_window(dialog)
        return dialog.user_input

    def show_error_dialog(self, message):
        dialog = ErrorDialog(self, message)
        self.wait_window(dialog)


class UserInputDialog(tk.Toplevel):
    def __init__(self, parent, prompt):
        super().__init__(parent)
        self.title("Input")
        self.geometry("300x100")

        self.user_input = tk.StringVar()

        prompt_label = tk.Label(self, text=prompt)
        prompt_label.pack()

        input_entry = tk.Entry(self, textvariable=self.user_input)
        input_entry.pack()

        confirm_button = tk.Button(self, text="OK", command=self.destroy)
        confirm_button.pack()


class ErrorDialog(tk.Toplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.title("Error")
        self.geometry("300x100")

        message_label = tk.Label(self, text=message)
        message_label.pack()

        ok_button = tk.Button(self, text="OK", command=self.destroy)
        ok_button.pack()


if interface:
    app = MetadataEditorApp()
    app.mainloop()
