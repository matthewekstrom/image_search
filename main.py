import glob
import tkinter as tk
from tkinter import filedialog, StringVar

import customtkinter as ctk
import cv2
import numpy as np
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
        self.result_image_path = None
        self.result_image = None
        self.result_image_label = None

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("image files", (".png", ".jpg"))])
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            # self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            # Change displayed image size to keep UI consistent
            frame_width = self.left_frame.winfo_width()
            frame_height = self.left_frame.winfo_height()
            dark_img = add_image_padding(image_rgb, frame_width / frame_height, (35, 35, 35))
            light_img = add_image_padding(image_rgb, frame_width / frame_height, (235, 235, 235))

            # Show selected image
            img = ctk.CTkImage(dark_image=Image.fromarray(dark_img), light_image=Image.fromarray(light_img), size=(frame_width, frame_height))
            if self.image_label:
                self.image_label.destroy()
            self.image_label = ctk.CTkLabel(self.left_frame, image=img, text="")
            self.image_label.pack()

            # Show image file name
            displayed_img_name = self.image_path[self.image_path.rfind('/') + 1:]
            if len(displayed_img_name) > 30:
                displayed_img_name = displayed_img_name[:19] + "..." + displayed_img_name[-8:]
            self.image_text.set(displayed_img_name)
            print(self.image_path)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            # Show selected folder name
            displayed_folder_name = self.folder_path[self.folder_path.rfind('/') + 1:]
            if len(displayed_folder_name) > 30:
                displayed_folder_name = displayed_folder_name[:19] + "..." + displayed_folder_name[-8:]
            self.folder_text.set(displayed_folder_name)
            print(self.folder_path)

    def find_closest_match(self):
        # Check if an image is not selected
        if self.image_path is None:
            self.image_text.set("Select an Image")
        # Check if a folder is not selected
        if self.folder_path is None:
            self.folder_text.set("Select a Folder")

        if self.image_path and self.folder_path:
            # Get filenames and images from folder
            filenames = glob.glob(f"{self.folder_path}/*.png")
            filenames.sort()
            folder_images = []
            ind = 0
            print("Loading Images...")
            while ind < len(filenames):
                img = cv2.imread(filenames[ind])
                if img is not None:
                    folder_images.append(img)
                    ind += 1
                else:
                    filenames.pop(ind)

            # Search folder for most similar image
            print("Searching...")
            result_index = get_most_similar_image(self.image, folder_images, compare_with_color=True)
            result_rgb = cv2.cvtColor(cv2.imread(filenames[result_index]), cv2.COLOR_BGR2RGB)
            self.result_image_path = filenames[result_index]
            self.result_image = result_rgb
            print("Image Path: " + self.result_image_path)

            # Change displayed image size
            frame_width = self.right_frame.winfo_width()
            frame_height = self.right_frame.winfo_height()
            dark_img = add_image_padding(self.result_image, frame_width / frame_height, (35, 35, 35))
            light_img = add_image_padding(self.result_image, frame_width / frame_height, (235, 235, 235))

            # Show result
            img = ctk.CTkImage(dark_image=Image.fromarray(dark_img), light_image=Image.fromarray(light_img), size=(frame_width, frame_height))
            if self.result_image_label:
                self.result_image_label.destroy()
            self.result_image_label = ctk.CTkLabel(self.right_frame, image=img, text="")
            self.result_image_label.pack()

            # Show image file path
            folder_name = self.folder_text.get()
            file_name = self.result_image_path[self.result_image_path.rfind('/') + 1:]
            if (len(folder_name) + len(file_name)) > 30:
                if len(folder_name) > 15:
                    folder_name = folder_name[:4] + "..." + folder_name[-8:]
                if len(file_name) > 15:
                    file_name = file_name[:4] + "..." + file_name[-8:]
            self.folder_text.set(folder_name + "/" + file_name)


def add_image_padding(image, frame_ratio, padding_color=(0, 0, 0)):
    height, width, _ = image.shape
    image_ratio = width / height

    if image_ratio == frame_ratio:
        return image
    if image_ratio < frame_ratio:  # If image is taller than frame, pad the sides
        new_width = int(height * frame_ratio)
        padding = int((new_width - width) / 2)
        padded_image = cv2.copyMakeBorder(image, 0, 0, padding, padding, cv2.BORDER_CONSTANT, value=padding_color)
    else:  # If image is wider than frame, pad the top and bottom
        new_height = int(width / frame_ratio)
        padding = int((new_height - height) / 2)
        padded_image = cv2.copyMakeBorder(image, padding, padding, 0, 0, cv2.BORDER_CONSTANT, value=padding_color)
    return padded_image


def mse(image_1, image_2, compare_with_color):
    # image_1 and image_2 should have the same dimensions
    if not compare_with_color:
        # Converting to grayscale gives faster comparisons
        image_1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
        image_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)

    # Calculate the Mean Squared Error of the two images
    # (Similar images will have a lower error value)
    difference = np.sum((image_1.astype("float") - image_2.astype("float")) ** 2)
    difference /= float(image_1.shape[0] * image_1.shape[1])
    # print("Difference: " + str(difference))
    return difference


def get_most_similar_image(image, candidates, compare_with_color=False):
    image_height, image_width, _ = image.shape
    scaled_width = 24
    scaled_height = int(scaled_width * (image_height / image_width))
    scaled_image = cv2.resize(image, (scaled_width, scaled_height), interpolation=cv2.INTER_AREA)
    image_index, closest_match = 0, 1000000

    # Compare with every candidate image
    for i in range(len(candidates)):
        # Stretch each candidate image to dimensions of selected image
        scaled_candidate = cv2.resize(candidates[i], (scaled_width, scaled_height), interpolation=cv2.INTER_AREA)
        comparison = mse(scaled_image, scaled_candidate, compare_with_color)
        if comparison < closest_match:
            closest_match = comparison
            image_index = i
        # If images are nearly identical, stop searching
        if closest_match < 200:
            break
    print("Lowest Difference: " + str(closest_match))
    print("Image Index: " + str(image_index))
    return image_index


if __name__ == "__main__":
    app = App()
    app.mainloop()
