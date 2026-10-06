import cv2
import easyocr
import os
import re
import csv

DATASET_DIR = "data/Dataset/Dataset/test"
RESULTS_DIR = "data/test/results"

os.makedirs(RESULTS_DIR, exist_ok=True)

OUTPUT_CSV = os.path.join(
    RESULTS_DIR,
    "detection_results.csv"
)

print("=" * 60)
print("230-IMAGE BIC DETECTION EXPERIMENT")
print("=" * 60)

print("\nLoading EasyOCR...")
reader = easyocr.Reader(["en"], gpu=False)
print("EasyOCR loaded.")

# Get all image files
image_files = [
    f for f in os.listdir(DATASET_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

image_files.sort()

print(f"\nImages found: {len(image_files)}")

results_table = []

for index, filename in enumerate(image_files, start=1):

    print(
        f"\n[{index}/{len(image_files)}] "
        f"Processing: {filename}"
    )

    image_path = os.path.join(
        DATASET_DIR,
        filename
    )

    image = cv2.imread(image_path)

    if image is None:
        print("  ERROR: Could not load image.")

        results_table.append([
            filename,
            "ERROR",
            "",
            "",
            ""
        ])

        continue

    results = reader.readtext(image)

    candidates = []

    # Store EasyOCR detections
    for result in results:

        bbox, text, confidence = result

        x_coords = [
            int(point[0])
            for point in bbox
        ]

        y_coords = [
            int(point[1])
            for point in bbox
        ]

        x1 = min(x_coords)
        y1 = min(y_coords)
        x2 = max(x_coords)
        y2 = max(y_coords)

        cleaned = re.sub(
            r"[^A-Z0-9]",
            "",
            text.upper()
        )

        candidates.append({
            "text": cleaned,
            "original": text,
            "confidence": confidence,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        })

    detection_method = "NONE"
    detected_text = ""
    detected_confidence = ""

    # --------------------------------------------------
    # METHOD 1:
    # Look for a 4-letter prefix + 6-digit serial
    # on the same horizontal line.
    # --------------------------------------------------

    for prefix in candidates:

        if not re.fullmatch(
            r"[A-Z]{4}",
            prefix["text"]
        ):
            continue

        for serial in candidates:

            if not re.fullmatch(
                r"\d{5,8}",
                serial["text"]
            ):
                continue

            if serial["x1"] <= prefix["x1"]:
                continue

            prefix_center_y = (
                prefix["y1"] +
                prefix["y2"]
            ) / 2

            serial_center_y = (
                serial["y1"] +
                serial["y2"]
            ) / 2

            vertical_difference = abs(
                prefix_center_y -
                serial_center_y
            )

            if vertical_difference > 25:
                continue

            detection_method = "PREFIX_SERIAL"

            detected_text = (
                prefix["text"] +
                " " +
                serial["text"]
            )

            detected_confidence = round(
                (
                    prefix["confidence"] +
                    serial["confidence"]
                ) / 2,
                3
            )

            break

        if detection_method != "NONE":
            break

    # --------------------------------------------------
    # METHOD 2:
    # Look for a detection containing a possible
    # container ID structure.
    # --------------------------------------------------

    if detection_method == "NONE":

        for candidate in candidates:

            # Remove spaces and punctuation
            text = candidate["text"]

            # Check for 4 letters followed by digits
            match = re.search(
                r"[A-Z]{4}\d{6,8}",
                text
            )

            if match:

                detection_method = "WHOLE_ID"

                detected_text = match.group(0)

                detected_confidence = round(
                    candidate["confidence"],
                    3
                )

                break

    # --------------------------------------------------
    # METHOD 3:
    # Six-digit serial anchor
    # --------------------------------------------------

    if detection_method == "NONE":

        for candidate in candidates:

            if re.fullmatch(
                r"\d{5,8}",
                candidate["text"]
            ):

                detection_method = "SERIAL_ONLY"

                detected_text = candidate["text"]

                detected_confidence = round(
                    candidate["confidence"],
                    3
                )

                break

    # --------------------------------------------------
    # Store result
    # --------------------------------------------------

    if detection_method == "NONE":

        print("  Detection: NO")

        results_table.append([
            filename,
            "NO",
            "NONE",
            "",
            ""
        ])

    else:

        print("  Detection: YES")
        print(f"  Method: {detection_method}")
        print(f"  Text: {detected_text}")
        print(f"  Confidence: {detected_confidence}")

        results_table.append([
            filename,
            "YES",
            detection_method,
            detected_text,
            detected_confidence
        ])


# ------------------------------------------------------
# Save CSV
# ------------------------------------------------------

with open(
    OUTPUT_CSV,
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    writer = csv.writer(csv_file)

    writer.writerow([
        "filename",
        "detected",
        "method",
        "text",
        "confidence"
    ])

    writer.writerows(results_table)


# ------------------------------------------------------
# Summary
# ------------------------------------------------------

total = len(results_table)

detected = sum(
    1
    for row in results_table
    if row[1] == "YES"
)

not_detected = sum(
    1
    for row in results_table
    if row[1] == "NO"
)

errors = sum(
    1
    for row in results_table
    if row[1] == "ERROR"
)

if total > 0:
    detection_rate = (
        detected / total
    ) * 100
else:
    detection_rate = 0


print("\n" + "=" * 60)
print("EXPERIMENT COMPLETE")
print("=" * 60)

print(f"Total images:     {total}")
print(f"Detected:         {detected}")
print(f"Not detected:     {not_detected}")
print(f"Errors:           {errors}")
print(f"Detection rate:   {detection_rate:.2f}%")

print("\nResults saved to:")
print(OUTPUT_CSV)

print("=" * 60)