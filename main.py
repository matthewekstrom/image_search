import tkinter as tk
from tkinter import filedialog, StringVar
import customtkinter as ctk
import cv2
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Main window
        self.title("Image Search")
        self.geometry("750x500")
        self.minsize(700, 500)
        ctk.set_appearance_mode("dark")

        # Configure grid layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)

        # Add image frames
        self.left_frame = ctk.CTkFrame(self, width=300, height=220, fg_color=("#d3d3d3", "#333333"), border_width=2)
        self.left_frame.grid(column=0, row=1, pady=10)
        self.right_frame = ctk.CTkFrame(self, width=300, height=220, fg_color=("#d3d3d3", "#333333"), border_width=2)
        self.right_frame.grid(column=1, row=1, pady=10)

        # Add buttons
        self.select_image_button = ctk.CTkButton(self, text="Select Image", fg_color="#00858c", command=self.select_image)
        self.select_image_button.grid(column=0, row=2, sticky=tk.N)
        self.select_folder_button = ctk.CTkButton(self, text="Select Folder", fg_color="#00858c", command=self.select_folder)
        self.select_folder_button.grid(column=1, row=2, sticky=tk.N)
        self.find_closest_match_button = ctk.CTkButton(self, text="Find Closest Match", command=self.find_closest_match)
        self.find_closest_match_button.grid(row=3, sticky=tk.N, columnspan=2, pady=20)

        # Add text labels
        self.image_text = StringVar()
        image_text_label = ctk.CTkLabel(self, textvariable=self.image_text)
        image_text_label.grid(column=0, row=0, sticky=tk.S)
        self.folder_text = StringVar()
        folder_text_label = ctk.CTkLabel(self, textvariable=self.folder_text)
        folder_text_label.grid(column=1, row=0, sticky=tk.S)

        # Variables for file paths and images
        self.image_path = None
        self.image = None
        self.image_label = None
        self.folder_path = None

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("image files", (".png", ".jpg"))])
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            frame_width = self.left_frame.winfo_width()
            frame_height = self.left_frame.winfo_height()
            dark_img = self.add_padding(self.image, frame_width / frame_height, (35, 35, 35))
            light_img = self.add_padding(self.image, frame_width / frame_height, (235, 235, 235))

            img = ctk.CTkImage(dark_image=Image.fromarray(dark_img), light_image=Image.fromarray(light_img), size=(frame_width, frame_height))
            if self.image_label:
                self.image_label.destroy()
            self.image_label = ctk.CTkLabel(self.left_frame, image=img, text="")
            self.image_label.pack()

            displayed_img_name = self.image_path[self.image_path.rfind('/') + 1:]
            if len(displayed_img_name) > 25:
                displayed_img_name = displayed_img_name[:16] + "..." + displayed_img_name[-6:]

            self.image_text.set(displayed_img_name)
            print(self.image_path)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        displayed_folder_name = self.folder_path[self.folder_path.rfind('/') + 1:]
        if len(displayed_folder_name) > 25:
            displayed_folder_name = displayed_folder_name[:16] + "..." + displayed_folder_name[-6:]

        self.folder_text.set(displayed_folder_name)
        print(self.folder_path)

    def add_padding(self, image, frame_ratio, padding_color=(0, 0, 0)):
        height, width, _ = image.shape
        image_ratio = width / height

        if image_ratio == frame_ratio:
            return image
        if image_ratio < frame_ratio:
            new_width = int(height * frame_ratio)
            padding = int((new_width - width) / 2)
            padded_image = cv2.copyMakeBorder(image, 0, 0, padding, padding, cv2.BORDER_CONSTANT, value=padding_color)
        else:
            new_height = int(width / frame_ratio)
            padding = int((new_height - height) / 2)
            padded_image = cv2.copyMakeBorder(image, padding, padding, 0, 0, cv2.BORDER_CONSTANT, value=padding_color)
        return padded_image

    def find_closest_match(self):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
