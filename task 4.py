import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import numpy as np
import cv2

file_path = ""

def convert_to_sketch(image_path, sketch_intensity):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_gray_image = 255 - gray_image
    blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)
    inverted_blurred_image = 255 - blurred_image
    pencil_sketch_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)
    pencil_sketch_image = cv2.multiply(pencil_sketch_image, sketch_intensity / 100)
    return pencil_sketch_image

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", ".jpg;.jpeg;.png;.bmp")])
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(image)
        original_label.config(image=photo)
        original_label.image = photo
        sketch_button.config(state=tk.NORMAL)
        sketch_intensity_scale.config(state=tk.NORMAL)
        sketch_intensity_scale.set(50)

def save_sketch(sketch_image):
    if sketch_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", ".png")])
        if save_path:
            
            sketch_image_np = cv2.cvtColor(np.array(sketch_image), cv2.COLOR_RGB2BGR)
            cv2.imwrite(save_path, sketch_image_np)
            print("Sketch successfully saved.")
        else:
            print("Save canceled.")
def convert_and_display_sketch():
    if file_path:
        sketch_intensity = sketch_intensity_scale.get()
        sketch_image = convert_to_sketch(file_path, sketch_intensity)
        sketch_image = cv2.cvtColor(sketch_image, cv2.COLOR_GRAY2RGB)
        sketch_image = Image.fromarray(sketch_image)
        sketch_image.thumbnail((400, 400))
        sketch_photo = ImageTk.PhotoImage(sketch_image)
        sketch_label.config(image=sketch_photo)
        sketch_label.image = sketch_photo
        save_button.config(state=tk.NORMAL, command=lambda: save_sketch(sketch_image))
    else:
        print("Please select an image first.")

root = tk.Tk()
root.title("Image to Sketch Converter")

original_label = tk.Label(root)
original_label.pack(pady=10)

sketch_intensity_label = tk.Label(root, text="Sketch Intensity:")
sketch_intensity_label.pack()

sketch_intensity_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=200, state=tk.DISABLED)
sketch_intensity_scale.pack()

open_button = tk.Button(root, text="Open Image", command=open_file)
open_button.pack(pady=5)

sketch_button = tk.Button(root, text="Convert to Sketch", command=convert_and_display_sketch, state=tk.DISABLED)
sketch_button.pack(pady=5)

sketch_label = tk.Label(root)
sketch_label.pack(pady=10)

save_button = tk.Button(root, text="Save Sketch", state=tk.DISABLED)
save_button.pack(pady=5)

root.mainloop()
