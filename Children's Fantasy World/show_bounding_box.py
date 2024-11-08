import sys
import os
import colorsys
sys.path.append("../Common Module")
from load_data import LoadData
from write_data import WriteData
from PIL import Image, ImageDraw

# Define bounding boxes and labels (new structure with potential scaling)
annotations = [
    "我在這張圖片中看到了建築工人、建築物、梯子、推土機和吊車",
    [[50, 450, 260, 900], "worker"],
    [[260, 600, 390, 930], "worker"],
    [[460, 300, 570, 650], "worker"],
    [[570, 220, 660, 490], "worker"],
    [[680, 290, 760, 480], "worker"],
    [[70, 0, 320, 600], "building"],
    [[320, 70, 470, 999], "building"],
    [[470, 0, 810, 999], "building"],
    [[810, 440, 1000, 880], "building"],
    [[0, 650, 90, 1000], "ladder"],
    [[760, 0, 910, 270], "ladder"],
    [[640, 730, 820, 950], "bulldozer"],
    [[520, 0, 740, 310], "crane"]
]

# Use a set to collect unique labels
unique_labels = set(label for _, label in annotations[1:])

# Generate equally spaced colors based on the number of unique labels
def generate_colors(n):
    """Generate `n` equally spaced colors in HSL space and convert to RGB."""
    colors = []
    for i in range(n):
        hue = i / n  # Equally spaced hues
        lightness = 0.5  # Fixed lightness for balanced color
        saturation = 0.7  # Fixed saturation for vivid colors
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        # Convert to hex color format
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
# 1000 is magic number don't move
scale_x = actual_width / 1000
scale_y = actual_height / 1000

# Draw bounding boxes with labels, applying scaling if needed
for bbox in annotations[1:]:  # Skip the first entry (text description)
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
        draw.text((x1, y1), label, fill=color)

# Save the output image with bounding boxes
writer = WriteData(prefix="bbox")
writer.save_img_PIL(image, image_path, attached_data=annotations, attached_data_name="response.txt")
