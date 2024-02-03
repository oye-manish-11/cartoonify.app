import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Function to cartoonize an image
def cartoonize_image(image):
    # Increase the parameters for a higher resolution cartoon image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, 7)  # Increased kernel size for better smoothing
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(image, 9, 350, 350)  # Increased parameters for more color preservation
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

# Function to process user input image and display it
def process_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

    if file_path:
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cartoon_image = cartoonize_image(image)
        
        # Resize the cartoon image to a higher resolution
        cartoon_image = cv2.resize(cartoon_image, (image.shape[1] * 2, image.shape[0] * 2))  # Double the resolution
        
        pil_image = Image.fromarray(cartoon_image)
        photo = ImageTk.PhotoImage(pil_image)
        image_label.config(image=photo)
        image_label.image = photo
        
        # Save the cartoonified image with a high resolution
        cartoon_image_pil = Image.fromarray(cartoon_image)
        cartoon_image_pil.save("cartoonified_image_hd.png")

# Function to download the cartoonified image
def download_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        cartoon_image = Image.open("cartoonified_image_hd.png")
        cartoon_image.save(file_path)

root = tk.Tk()
root.title("Image Cartoonizer")

header_label = tk.Label(root, text="Cartoonify Your Image", font=("Helvetica", 18))
header_label.pack(pady=10)

browse_button = tk.Button(root, text="Browse Image", command=process_image, bg="#4CAF50", fg="white", padx=10, pady=5)
browse_button.pack(pady=5)

download_button = tk.Button(root, text="Download Cartoonified Image", command=download_image, bg="#4CAF50", fg="white", padx=10, pady=5)
download_button.pack(pady=5)

image_label = tk.Label(root)
image_label.pack(padx=10, pady=10)

root.mainloop()
