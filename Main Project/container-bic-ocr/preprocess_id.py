import cv2
import os

INPUT_PATH = "data/test/detected/container_id_crop.jpg"
OUTPUT_PATH = "data/test/detected/container_id_enhanced.jpg"

# Load crop
image = cv2.imread(INPUT_PATH)

if image is None:
    print("ERROR: Could not load the container ID crop.")
    exit()

print(f"Original size: {image.shape[1]} x {image.shape[0]}")

# Upscale the image
scale = 4

upscaled = cv2.resize(
    image,
    None,
    fx=scale,
    fy=scale,
    interpolation=cv2.INTER_CUBIC
)

# Convert to grayscale
gray = cv2.cvtColor(
    upscaled,
    cv2.COLOR_BGR2GRAY
)

# Improve contrast
enhanced = cv2.equalizeHist(gray)

# Save result
cv2.imwrite(
    OUTPUT_PATH,
    enhanced
)

print(f"Enhanced image saved to:")
print(OUTPUT_PATH)

print(f"Enhanced size: {enhanced.shape[1]} x {enhanced.shape[0]}")