import sys
import os
sys.path.append("../Common Module")
from load_data import LoadData
from write_data import WriteData
from PIL import Image, ImageDraw


from PIL import Image, ImageDraw

# Define bounding boxes and labels
annotations = [
    [[0, 0, 330, 600], "building"],
    [[300, 0, 1000, 600], "shop"],
    [[270, 0, 570, 600], "stairs"],
    [[0, 570, 1000, 1000], "people"],
    [[50, 520, 220, 720], "people"],
    [[750, 540, 950, 700], "people"],
    [[470, 630, 650, 820], "people"],
    [[200, 590, 500, 1000], "people"],
    [[630, 740, 810, 980], "people"],
    [[530, 310, 580, 470], "yellow sign"],
    [[0, 170, 30, 200], "red lantern"]
]

# Define colors for each class
colors = {
    "building": "blue",
    "shop": "green",
    "stairs": "orange",
    "people": "purple",
    "yellow sign": "yellow",
    "red lantern": "red"
}

# Load the image
image_path = 'testimgs/941.jpg'
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# Get the actual dimensions of the image
actual_width, actual_height = image.size

# Scaling factor based on the annotated dimensions (1000x1000)
scale_x = actual_width / 1000
scale_y = actual_height / 1000

# Draw scaled bounding boxes with labels
for bbox, label in annotations:
    x1, y1, x2, y2 = bbox
    # Scale the bounding box coordinates
    x1 = int(x1 * scale_x)
    y1 = int(y1 * scale_y)
    x2 = int(x2 * scale_x)
    y2 = int(y2 * scale_y)
    color = colors.get(label, "white")  # Default to white if label not in colors
    draw.rectangle([x1, y1, x2, y2], outline=color, width=5)
    draw.text((x1, y1), label, fill=color)

# Save and display the output image
output_path = 'test_with_bboxes_scaled.png'
image.save(output_path)
output_path

