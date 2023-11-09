import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

root = ctk.CTk()
root.title("Image Search")
root.geometry("700x500")
root.minsize(700, 500)
ctk.set_appearance_mode("Dark")


def select_file():
    file_path = filedialog.askopenfilename()


def select_folder():
    folder_path = filedialog.askdirectory()


def find_closest_match():
    pass


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=3)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=2)

rect = ctk.CTkFrame(root, width=280, height=200, border_width=2)
rect.grid(column=0, row=1, pady=10)

# Create file selection button
select_file_button = ctk.CTkButton(root, text="Select Image", command=select_file)
select_file_button.grid(column=0, row=0, sticky=tk.S)

rect2 = ctk.CTkFrame(root, width=280, height=200, border_width=2)
rect2.grid(column=1, row=1, pady=10)

# Create folder selection button
folder_button = ctk.CTkButton(root, text="Select Folder", command=select_folder)
folder_button.grid(column=1, row=0, sticky=tk.S)

folder_button = ctk.CTkButton(root, text="Find Closest Match", command=find_closest_match)
folder_button.grid(row=2, sticky=tk.N, columnspan=2, pady=20)

root.mainloop()
