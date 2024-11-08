import sys
import os
import colorsys
import json
sys.path.append("../Common Module")
from load_data import LoadData
from write_data import WriteData
from PIL import Image, ImageDraw, ImageFont

# Load annotations from response.txt
with open('response.txt', 'r', encoding='utf-8') as file:
    annotations = json.load(file)

# Extract text description and bounding boxes
description = annotations[0]
bounding_boxes = annotations[1:]

# Use a set to collect unique labels
unique_labels = set(label for _, label in bounding_boxes)

# Generate equally spaced colors based on the number of unique labels
def generate_colors(n):
    """Generate `n` equally spaced colors in HSL space and convert to RGB."""
    colors = []
    for i in range(n):
        hue = i / n  # Equally spaced hues
        lightness = 0.5  # Fixed lightness for balanced color
        saturation = 0.7  # Fixed saturation for vivid colors
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        colors.append('#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)))
    return colors

# Assign colors to each unique label
label_to_color = {label: color for label, color in zip(unique_labels, generate_colors(len(unique_labels)))}

# Load the uploaded image
image_path = 'testimgs/優等_1051.jpg'
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# Actual dimensions of the image
actual_width, actual_height = image.size

# Calculate scaling factors
# 1000 is magic number don't modify
scale_x = actual_width / 1000
scale_y = actual_height / 1000

# Set font size and load font
font_size = 24  # Increase font size for better visibility
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except IOError:
    font = ImageFont.load_default()  # Fallback if font file is not found

# Draw bounding boxes with labels, applying scaling
for bbox in bounding_boxes:
    if len(bbox) == 2 and len(bbox[0]) == 4:  # Ensure bbox structure is correct
        coords, label = bbox[0], bbox[1]
        x1, y1, x2, y2 = coords
        
        # Apply scaling
        x1 = int(x1 * scale_x)
        y1 = int(y1 * scale_y)
        x2 = int(x2 * scale_x)
        y2 = int(y2 * scale_y)
        
        # Get the assigned color for the label
        color = label_to_color[label]
        draw.rectangle([x1, y1, x2, y2], outline=color, width=4)  # Thicker border

        # Calculate text bounding box
        text_bbox = draw.textbbox((x1, y1), label, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        
        # Draw background for text
        text_bg = [(x1, y1 - text_height - 4), (x1 + text_width + 4, y1)]
        draw.rectangle(text_bg, fill=color)
        
        # Draw label with white text
        draw.text((x1 + 2, y1 - text_height - 2), label, fill="white", font=font)

# Save the output image with bounding boxes
writer = WriteData(prefix="bbox")
writer.save_img_PIL(image, image_path, attached_data=annotations, attached_data_name="response.txt")
