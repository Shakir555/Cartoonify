# Libraries
import cv2

# Resize to fit the window
def resize_to_fit_window(image, width = 400, height = 300):
    # Resize an image to fit the GUI Window
    return cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)

# Read Image Path
def read_image(image_path):
    # Read an image from the given path
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Error: Unable to read the image file '{image_path}'")
    return image

# Apply Cartoon Style
def apply_cartoon_style(image, style):
    # Apply a cartoon effect based on the selected style
    if style == 1:
        return cv2.stylization(image, sigma_s = 150, sigma_r = 0.25)
    elif style == 2:
        return cv2.stylization(image, sigma_s = 60, sigma_r = 0.5)
    else:
        raise ValueError("Invalid Cartoon Style selected")
