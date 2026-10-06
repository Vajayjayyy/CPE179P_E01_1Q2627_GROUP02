import cv2
import easyocr
import os

DATASET_DIR = "data/Dataset/Dataset/test"

IMAGE_FILES = [
    "116_jpg.rf.7782d98a64635f5cb28411f3c752bb2e.jpg",
    "125_jpg.rf.18e9adb6c5b8c7a7a31e32fcb62e6840.jpg",
    "139_jpg.rf.66f10748c2b3977295cbd0a8a3740bd9.jpg",
    "140_jpg.rf.b43a95dc01882b42d23e791b4b54878c.jpg",
    "156_jpg.rf.4a41615f513c40c5d8397696a317b2b1.jpg",
]

print("=" * 60)
print("EASYOCR DETECTION COORDINATE TEST")
print("=" * 60)

print("\nLoading EasyOCR...")
reader = easyocr.Reader(["en"], gpu=False)
print("EasyOCR loaded.")

for index, filename in enumerate(IMAGE_FILES, start=1):

    image_path = os.path.join(DATASET_DIR, filename)

    print("\n" + "=" * 60)
    print(f"IMAGE {index}: {filename}")
    print("=" * 60)

    image = cv2.imread(image_path)

    if image is None:
        print("ERROR: Could not load image.")
        continue

    results = reader.readtext(image)

    print(f"Detected regions: {len(results)}")

    for detection_number, result in enumerate(results, start=1):

        bbox, text, confidence = result

        x_coordinates = [int(point[0]) for point in bbox]
        y_coordinates = [int(point[1]) for point in bbox]

        x1 = min(x_coordinates)
        y1 = min(y_coordinates)
        x2 = max(x_coordinates)
        y2 = max(y_coordinates)

        print(
            f"{detection_number}. "
            f"'{text}' "
            f"(confidence: {confidence:.3f}) "
            f"BOX=({x1},{y1}) → ({x2},{y2})"
        )

print("\n" + "=" * 60)
print("COORDINATE TEST COMPLETE")
print("=" * 60)