import os
import shutil
import tkinter as tk

from tkinter import filedialog, messagebox


# File categories
FILE_TYPES = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif",
        ".webp", ".svg"
    ],
    "Documents": [
        ".pdf", ".doc", ".docx", ".txt",
        ".xlsx", ".xls", ".pptx", ".csv"
    ],
    "Videos": [
        ".mp4", ".mkv", ".avi", ".mov"
    ],
    "Audio": [
        ".mp3", ".wav", ".aac", ".flac"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz"
    ],
}


selected_folder = ""


def select_folder():
    global selected_folder

    folder = filedialog.askdirectory(
        title="Select a folder to organize"
    )

    if folder:
        selected_folder = folder
        folder_label.config(text=folder)
        status_label.config(text="Status: Folder selected")


def organize_files():
    if not selected_folder:
        messagebox.showwarning(
            "Warning",
            "Please select a folder first!"
        )
        return

    moved_count = 0
    error_count = 0

    try:
        for filename in os.listdir(selected_folder):
            source = os.path.join(selected_folder, filename)

            # Skip directories
            if not os.path.isfile(source):
                continue

            extension = os.path.splitext(filename)[1].lower()

            category = "Others"

            for folder_name, extensions in FILE_TYPES.items():
                if extension in extensions:
                    category = folder_name
                    break

            destination_folder = os.path.join(
                selected_folder,
                category
            )

            os.makedirs(destination_folder, exist_ok=True)

            destination = os.path.join(
                destination_folder,
                filename
            )

            # Avoid overwriting existing files
            if os.path.exists(destination):
                error_count += 1
                continue

            try:
                shutil.move(source, destination)
                moved_count += 1
            except OSError:
                error_count += 1

        status_label.config(
            text=f"Status: Organized {moved_count} files"
        )

        messagebox.showinfo(
            "Completed",
            f"Successfully organized: {moved_count} files\n"
            f"Skipped or failed: {error_count} files"
        )

    except OSError as error:
        messagebox.showerror(
            "Error",
            f"Could not organize folder:\n{error}"
        )


# Create main window
root = tk.Tk()
root.title("File Organizer")
root.geometry("500x300")
root.resizable(False, False)


# Heading
title_label = tk.Label(
    root,
    text="FILE ORGANIZER",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=15)


# Description
description_label = tk.Label(
    root,
    text="Organize your files with one click!"
)
description_label.pack()


# Folder selection button
select_button = tk.Button(
    root,
    text="Select Folder",
    command=select_folder,
    width=20
)
select_button.pack(pady=10)


# Selected folder display
folder_label = tk.Label(
    root,
    text="No folder selected",
    wraplength=450
)
folder_label.pack(pady=5)


# Organize button
organize_button = tk.Button(
    root,
    text="ORGANIZE FILES",
    command=organize_files,
    width=25,
    height=2,
    bg="#2E8B57",
    fg="white"
)
organize_button.pack(pady=10)


# Status display
status_label = tk.Label(
    root,
    text="Status: Ready"
)
status_label.pack(pady=5)


# Start application
root.mainloop()