import sys
import os
sys.path.append("../Common Module")
from load_data import LoadData
from write_data import WriteData
from PIL import Image, ImageDraw

# Define bounding boxes and labels (new structure with potential scaling)
annotations = [
    [800, 1067],  # Image dimensions
    [[350, 300, 450, 450], "person"],
    [[450, 340, 550, 450], "person"],
    [[200, 590, 500, 1000], "person"],
    [[450, 630, 650, 820], "person"],
    [[500, 820, 680, 1000], "person"],
    [[640, 740, 820, 970], "person"],
    [[740, 550, 990, 930], "person"],
    [[840, 710, 1000, 980], "person"],
    [[0, 770, 170, 920], "person"],
    [[50, 530, 220, 720], "person"],
    [[150, 430, 250, 550], "person"],
    [[220, 470, 320, 570], "person"],
    [[620, 540, 680, 660], "person"],
    [[850, 470, 960, 620], "person"],
    [[620, 420, 780, 540], "person"],
    [[750, 440, 830, 510], "person"],
    [[530, 310, 730, 480], "staircase"],
    [[0, 0, 350, 600], "building"],
    [[480, 0, 1000, 650], "building"],
    [[530, 310, 580, 480], "banner"],
    [[600, 360, 960, 420], "signboard"]
]

# Define colors for each class
colors = {
    "building": "blue",
    "shop": "green",
    "stairs": "orange",
    "person": "purple",
    "staircase": "brown",
    "banner": "pink",
    "signboard": "yellow"
}

# Load the uploaded image
image_path = 'testimgs/941.jpg'
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# Actual dimensions of the image
actual_width, actual_height = image.size

# Input dimensions from annotations
input_width, input_height = annotations[0]

# Calculate scaling factors
scale_x = actual_width / input_width
scale_y = actual_height / input_height

# Draw bounding boxes with labels, applying scaling if needed
for bbox in annotations[1:]:  # Skip the first entry (dimensions)
    if len(bbox) == 2 and len(bbox[0]) == 4:  # Ensure bbox structure is correct
        coords, label = bbox[0], bbox[1]
        x1, y1, x2, y2 = coords
        
        # Apply scaling if input dimensions don't match actual dimensions
        x1 = int(x1 * scale_x)
        y1 = int(y1 * scale_y)
        x2 = int(x2 * scale_x)
        y2 = int(y2 * scale_y)
        
        color = colors.get(label, "white")  # Default to white if label not in colors
        draw.rectangle([x1, y1, x2, y2], outline=color, width=4)  # Thicker border
        draw.text((x1, y1), label, fill=color)

# Save the output image with bounding boxes
writer = WriteData(prefix="bbox")
writer.save_img_PIL(image, image_path,attached_data=annotations,attached_data_name="response.txt")
