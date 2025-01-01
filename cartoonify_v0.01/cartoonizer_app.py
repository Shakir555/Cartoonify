# Libraries
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from cartoonizer_img import resize_to_fit_window, read_image, apply_cartoon_style
import threading

# CartoonizerApp
class CartoonizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cartoonizer")
        self.root.geometry("600x500")
        self.image = None
        self.image_path = None

        # Title Label
        self.label_title = tk.Label(root, text = "Select an Image to Cartoonize",
                                    font = ("Arial", 16))
        self.label_title.pack(pady = 10)

        # Image Display Area
        self.label_image = tk.Label(root)
        self.label_image.pack()

        # Browse Button
        self.button_browse = tk.Button(root, text = "Browse Image", command = self.browse_file)
        self.button_browse.pack(pady = 10)

        # Cartoon Style Buttons
        frame_styles = tk.LabelFrame(root, text = "Cartoon Styles", padx = 10, pady = 10)
        frame_styles.pack(pady = 10)

        # Style 1
        self.button_style_1 = tk.Button(frame_styles, text = "Style 1",
                                        command = lambda: self.apply_cartoon_effect_thread(1))
        self.button_style_1.grid(row = 0, column = 0, padx = 10)

        self.button_style_2 = tk.Button(frame_styles, text = "Style 2",
                                        command = lambda: self.apply_cartoon_effect_thread(2))
        self.button_style_2.grid(row = 0, column = 1, padx = 10)

        # Loading Label
        self.loading_label = tk.Label(root, text = "", font = ("Arial", 12), fg = "red")
        self.loading_label.pack(pady = 10)

    # Browse File
    def browse_file(self):
        # Browse file and select image
        filetypes = [("Image files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All files", "*.*")]
        self.image_path = filedialog.askopenfilename(title = "Select an Image File",
                                                     filetypes = filetypes)

        if self.image_path:
            try:
                self.image = read_image(self.image_path)
                self.display_image(self.image, "Original Image")
            except FileNotFoundError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "No file selected.")

    # Display Open CV Image on Tkinter
    def display_image(self, image, title = "Image"):
        # Display an Image in the Tkinter GUI
        resized = resize_to_fit_window(image)
        # Convert to RGB for Tkinter
        image_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image_rgb)
        imgtk = ImageTk.PhotoImage(image = img)
        self.label_image.config(image = imgtk)
        self.label_image.image = imgtk
        self.label_title.config(text = title)

    # Apply Cartoon Effect
    def apply_cartoon_effect(self, style):
        # Apply Cartoon Style to the selected image
        if self.image is None:
            messagebox.showerror("Error", "Please Select an Image First")
            return

        # Show loading Indicator
        self.loading_label.config(text = "Processing..")
        self.root.update_idletasks()

        try:
            cartoon_image = apply_cartoon_style(self.image, style)
            self.display_image(cartoon_image, f"Cartoon style {style}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        finally:
            # Hide Loading Indicator
            self.loading_label.config(text = " ")

    # Apply Cartoon Effect Thread
    def apply_cartoon_effect_thread(self, style):
        # Run apply cartoon effect in a seperate thread to avoid freezing the GUI
        threading.Thread(target=self.apply_cartoon_effect, args=(style,), daemon=True).start()

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = CartoonizerApp(root)
    root.mainloop()
