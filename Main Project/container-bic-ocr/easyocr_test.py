import cv2
import easyocr
import os

IMAGE_PATH = "data/test/Container1.jpg"
OUTPUT_DIR = "data/test/detected"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("CONTAINER BIC OCR - EASYOCR DETECTION TEST")
print("=" * 60)

# Load image
image = cv2.imread(IMAGE_PATH)

if image is None:
    print("ERROR: Could not load image.")
    print(IMAGE_PATH)
    exit()

print(f"Image loaded: {IMAGE_PATH}")
print(f"Image size: {image.shape[1]} x {image.shape[0]}")

# Make a copy for drawing detection boxes
boxed_image = image.copy()

# Load EasyOCR
print("\nLoading EasyOCR...")
reader = easyocr.Reader(["en"], gpu=False)
print("EasyOCR loaded.")

# Detect text
print("\nDetecting text...")
results = reader.readtext(image)

print(f"Detected regions: {len(results)}")

# Process detections
for i, result in enumerate(results):

    bbox, text, confidence = result

    print("\n--------------------------------")
    print(f"Detection #{i + 1}")
    print(f"Text: {text}")
    print(f"Confidence: {confidence:.3f}")
    print(f"Bounding box: {bbox}")

    # Convert bounding box points to integers
    points = []

    for point in bbox:
        x = int(point[0])
        y = int(point[1])
        points.append((x, y))

    # Draw bounding box
    cv2.polylines(
        boxed_image,
        [__import__("numpy").array(points)],
        True,
        (0, 255, 0),
        2
    )

    # Get rectangular crop coordinates
    x_coordinates = [point[0] for point in points]
    y_coordinates = [point[1] for point in points]

    x1 = max(0, min(x_coordinates))
    y1 = max(0, min(y_coordinates))
    x2 = min(image.shape[1], max(x_coordinates))
    y2 = min(image.shape[0], max(y_coordinates))

    # Crop detected text
    crop = image[y1:y2, x1:x2]

    if crop.size == 0:
        continue

    output_path = os.path.join(
        OUTPUT_DIR,
        f"crop_{i + 1}.jpg"
    )

    cv2.imwrite(output_path, crop)

    print(f"Saved crop: {output_path}")

# Save image with all detection boxes
boxed_image_path = os.path.join(
    OUTPUT_DIR,
    "detections.jpg"
)

cv2.imwrite(boxed_image_path, boxed_image)

print("\n========================================")
print(f"Detection image saved: {boxed_image_path}")
print("Detection complete.")
print("========================================")