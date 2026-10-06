import cv2
import easyocr
import os


IMAGE_PATH = "data/test/Container1.jpg"
OUTPUT_DIR = "data/test/detected"

os.makedirs(OUTPUT_DIR, exist_ok=True)


print("=" * 60)
print("AUTOMATIC BIC REGION DETECTION")
print("=" * 60)


# --------------------------------------------------
# 1. Load image
# --------------------------------------------------

image = cv2.imread(IMAGE_PATH)

if image is None:
    print("ERROR: Could not load image.")
    exit()

height, width = image.shape[:2]

print(f"Image loaded: {IMAGE_PATH}")
print(f"Image size: {width} x {height}")


# --------------------------------------------------
# 2. Load EasyOCR
# --------------------------------------------------

print("\nLoading EasyOCR...")

reader = easyocr.Reader(
    ["en"],
    gpu=False
)

print("EasyOCR loaded.")


# --------------------------------------------------
# 3. Detect text
# --------------------------------------------------

print("\nDetecting text...")

results = reader.readtext(image)

print(f"Detected regions: {len(results)}")


# --------------------------------------------------
# 4. Convert detections into rectangles
# --------------------------------------------------

detections = []

for result in results:

    bbox, text, confidence = result

    xs = [int(point[0]) for point in bbox]
    ys = [int(point[1]) for point in bbox]

    x1 = min(xs)
    y1 = min(ys)
    x2 = max(xs)
    y2 = max(ys)

    detections.append({
        "text": text,
        "confidence": confidence,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2
    })


# --------------------------------------------------
# 5. Find possible BIC candidates
# --------------------------------------------------

print("\nSearching for possible BIC regions...")

candidate_regions = []


for detection in detections:

    text = detection["text"].upper().replace(" ", "")

    # Look for a six-digit container serial number.
    # This will be our anchor.
    if len(text) != 6:
        continue

    if not text.isdigit():
        continue

    print(
        f"Possible serial number detected: "
        f"{text}"
    )

    # The serial number is our anchor.
    x1 = detection["x1"]
    y1 = detection["y1"]
    x2 = detection["x2"]
    y2 = detection["y2"]

    # Expand around the serial number.
    #
    # Left side:
    # captures the owner/equipment code (DAYU)
    #
    # Right side:
    # captures the ISO check digit (3)
    #
    # Vertical padding:
    # gives TrOCR some surrounding image context.

    padding_left = 60
    padding_right = 30
    padding_top = 8
    padding_bottom = 2

    crop_x1 = max(
        0,
        x1 - padding_left
    )

    crop_y1 = max(
        0,
        y1 - padding_top
    )

    crop_x2 = min(
        width,
        x2 + padding_right
    )

    crop_y2 = min(
        height,
        y2 + padding_bottom
    )

    candidate_regions.append(
        (
            crop_x1,
            crop_y1,
            crop_x2,
            crop_y2,
            text
        )
    )


# --------------------------------------------------
# 6. Save candidate regions
# --------------------------------------------------

if not candidate_regions:

    print("\nNo six-digit serial number detected.")
    print("No automatic BIC candidate was created.")

else:

    print(
        f"\nFound {len(candidate_regions)} "
        "possible BIC region(s)."
    )

    for index, candidate in enumerate(
        candidate_regions,
        start=1
    ):

        x1, y1, x2, y2, serial = candidate

        crop = image[
            y1:y2,
            x1:x2
        ]

        output_path = os.path.join(
            OUTPUT_DIR,
            f"auto_bic_candidate_{index}.jpg"
        )

        cv2.imwrite(
            output_path,
            crop
        )

        print("\n--------------------------------")
        print(f"Candidate #{index}")
        print(f"Serial anchor: {serial}")
        print(
            f"Coordinates: "
            f"({x1}, {y1}) → ({x2}, {y2})"
        )
        print(f"Saved: {output_path}")


print("\n========================================")
print("Automatic BIC detection complete.")
print("========================================")