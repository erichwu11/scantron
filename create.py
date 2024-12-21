import cv2.aruco as aruco
from PIL import Image, ImageDraw, ImageFont

# Constants
questions = 17
img_name = "exam.png"

# Generate ArUco marker images
def generate_marker(id, size=30):
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
    marker_img = aruco.generateImageMarker(aruco_dict, id, size)
    return marker_img

# Create a blank white image
img = Image.new('RGB', (360 + 30 * questions, 410), color='white')
d = ImageDraw.Draw(img)

# Row headers (0–9)
for i in range(10):  # Row labels (0–9)
    d.text((30, 80 + i * 30), str(i), fill=(0, 0, 0), anchor="mm")

d.text((180, 50), "ID", fill=(0, 0, 0), anchor="mm")
# Draw the ID columns (9 columns for ID bubbles)
for col in range(9):
    col_x = 60 + col * 30
    for row in range(10):  # Draw bubbles for each row (0–9)
        bubble_y = 80 + row * 30
        # x = 20, y = 14
        d.ellipse([(col_x - 10, bubble_y - 7), (col_x + 10, bubble_y + 7)], outline=(0, 0, 0))

# Draw a thin line between 9th and 10th column
d.line([(320, 30), (320, 360)], fill=(0, 0, 0), width=1)

for col in range(questions):
    col_x = 340 + col * 30
    d.text((col_x, 50), str(col + 1), fill=(0, 0, 0), anchor="mm")  # Label columns 1–10
    for row in range(10):  # Draw bubbles for each row (0–9)
        bubble_y = 80 + row * 30
        # if (row + col) % 2:
        #     d.ellipse([(col_x - 10, bubble_y - 7), (col_x + 10, bubble_y + 7)], outline=(0, 0, 0), fill=(0, 0, 0))
        # else:
        #     d.ellipse([(col_x - 10, bubble_y - 7), (col_x + 10, bubble_y + 7)], outline=(0, 0, 0))
        d.ellipse([(col_x - 10, bubble_y - 7), (col_x + 10, bubble_y + 7)], outline=(0, 0, 0))

# add marker to img
mark0 = Image.fromarray(generate_marker(0))
mark1 = Image.fromarray(generate_marker(1))
mark2 = Image.fromarray(generate_marker(2))
mark3 = Image.fromarray(generate_marker(7))

img.paste(mark0, (10, 10))
img.paste(mark1, (320 + 30 * questions, 10))
img.paste(mark2, (10, 370))
img.paste(mark3, (320 + 30 * questions, 370))

# new_size = (int(img.width * 0.9), int(img.height * 0.9))
# img_resized = img.resize(new_size, Image.LANCZOS)

# Save the image
img.save(img_name)
# img_resized.save("lol.png")
