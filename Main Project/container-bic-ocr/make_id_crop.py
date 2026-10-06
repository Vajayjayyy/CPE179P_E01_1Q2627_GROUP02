import cv2
import os

IMAGE_PATH = "data/test/Container1.jpg"
OUTPUT_DIR = "data/test/detected"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load original image
image = cv2.imread(IMAGE_PATH)

if image is None:
    print("ERROR: Could not load image.")
    exit()

print(f"Image size: {image.shape[1]} x {image.shape[0]}")

# Container ID area
# Based on the current image, the ID is around the upper-right/middle area.
x1 = 220
y1 = 70
x2 = 365
y2 = 95

# Crop the ID region
id_crop = image[y1:y2, x1:x2]

# Save crop
output_path = os.path.join(
    OUTPUT_DIR,
    "container_id_crop.jpg"
)

cv2.imwrite(output_path, id_crop)

print(f"Container ID crop saved to:")
print(output_path)