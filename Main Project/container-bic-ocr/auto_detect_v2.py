import cv2
import easyocr
import os
import re

DATASET_DIR = "data/Dataset/Dataset/test"
OUTPUT_DIR = "data/test/batch_candidates_v2"

IMAGE_FILES = [
    "116_jpg.rf.7782d98a64635f5cb28411f3c752bb2e.jpg",
    "125_jpg.rf.18e9adb6c5b8c7a7a31e32fcb62e6840.jpg",
    "139_jpg.rf.66f10748c2b3977295cbd0a8a3740bd9.jpg",
    "140_jpg.rf.b43a95dc01882b42d23e791b4b54878c.jpg",
    "156_jpg.rf.4a41615f513c40c5d8397696a317b2b1.jpg",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("AUTOMATIC BIC DETECTION V2")
print("=" * 60)

print("\nLoading EasyOCR...")
reader = easyocr.Reader(["en"], gpu=False)
print("EasyOCR loaded.")

for index, filename in enumerate(IMAGE_FILES, start=1):

    print("\n" + "=" * 60)
    print(f"IMAGE {index}: {filename}")
    print("=" * 60)

    image_path = os.path.join(DATASET_DIR, filename)
    image = cv2.imread(image_path)

    if image is None:
        print("ERROR: Could not load image.")
        continue

    results = reader.readtext(image)

    candidates = []

    for result in results:

        bbox, text, confidence = result

        x_coords = [int(point[0]) for point in bbox]
        y_coords = [int(point[1]) for point in bbox]

        x1 = min(x_coords)
        y1 = min(y_coords)
        x2 = max(x_coords)
        y2 = max(y_coords)

        cleaned = re.sub(r"[^A-Z0-9]", "", text.upper())

        candidates.append({
            "text": cleaned,
            "confidence": confidence,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        })

    found = False

    # Look for a 4-character prefix + 6-digit serial
    for prefix in candidates:

        if not re.fullmatch(r"[A-Z]{4}", prefix["text"]):
            continue

        for serial in candidates:

            if not re.fullmatch(r"\d{6}", serial["text"]):
                continue

            # Make sure prefix comes before serial
            if serial["x1"] <= prefix["x1"]:
                continue

            # Check horizontal alignment
            prefix_center_y = (prefix["y1"] + prefix["y2"]) / 2
            serial_center_y = (serial["y1"] + serial["y2"]) / 2

            vertical_difference = abs(
                prefix_center_y - serial_center_y
            )

            if vertical_difference > 25:
                continue

            # Create combined bounding box
            x1 = min(prefix["x1"], serial["x1"])
            y1 = min(prefix["y1"], serial["y1"])
            x2 = max(prefix["x2"], serial["x2"])
            y2 = max(prefix["y2"], serial["y2"])

            # Add padding
            padding_left = 15
            padding_right = 25
            padding_top = 8
            padding_bottom = 5

            crop_x1 = max(0, x1 - padding_left)
            crop_y1 = max(0, y1 - padding_top)
            crop_x2 = min(image.shape[1], x2 + padding_right)
            crop_y2 = min(image.shape[0], y2 + padding_bottom)

            crop = image[
                crop_y1:crop_y2,
                crop_x1:crop_x2
            ]

            output_path = os.path.join(
                OUTPUT_DIR,
                f"image_{index}_candidate.jpg"
            )

            cv2.imwrite(output_path, crop)

            print("\nBIC CANDIDATE FOUND")
            print(f"Prefix: {prefix['text']}")
            print(f"Serial: {serial['text']}")
            print(
                f"Vertical difference: "
                f"{vertical_difference:.1f}px"
            )
            print(f"Saved: {output_path}")

            found = True
            break

        if found:
            break

    if not found:
        print("\nNo prefix + serial pair found.")

print("\n" + "=" * 60)
print("AUTOMATIC DETECTION V2 COMPLETE")
print("=" * 60)