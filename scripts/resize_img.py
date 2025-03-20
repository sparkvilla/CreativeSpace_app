import os
from PIL import Image, ImageOps

image_path = "/home/diego/Downloads/MrMorning.jpg"

# Open and process the image
with Image.open(image_path) as img:
    # Make image square by cropping the center
    min_side = min(img.size)  # Get smallest dimension (to crop square)
    img = ImageOps.fit(img, (min_side, min_side), Image.LANCZOS)  # Crop to square

    # Resize to desired size (300x300)
    img = img.resize((300, 300), Image.LANCZOS)

    # Save the final image
    img.save(image_path)
