import cv2
import easyocr
import os

DATASET_DIR = "data/Dataset/Dataset/test"
OUTPUT_DIR = "data/test/failed_inspection"

IMAGE_FILES = [
    "139_jpg.rf.66f10748c2b3977295cbd0a8a3740bd9.jpg",
    "16-19_jpg.rf.776db4ee5aed2de0bb69a2ad07bf7540.jpg",
    "165_jpg.rf.719b15b9072e627bd9473b196d10275a.jpg",
    "200_jpg.rf.4f91d66d0dc2d43a81b03736d23c785d.jpg",
    "206_jpg.rf.cb0035e181b4b2dbcfe65c876e29f110.jpg",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("FAILED IMAGE INSPECTION")
print("=" * 60)

print("\nLoading EasyOCR...")
reader = easyocr.Reader(["en"], gpu=False)
print("EasyOCR loaded.")

for index, filename in enumerate(IMAGE_FILES, start=1):

    image_path = os.path.join(DATASET_DIR, filename)
    image = cv2.imread(image_path)

    print("\n" + "=" * 60)
    print(f"IMAGE {index}: {filename}")
    print("=" * 60)

    if image is None:
        print("ERROR: Could not load image.")
        continue

    results = reader.readtext(image)

    print(f"Detected regions: {len(results)}")

    # Draw all EasyOCR detections
    annotated = image.copy()

    for detection_number, result in enumerate(results, start=1):

        bbox, text, confidence = result

        points = [
            (int(point[0]), int(point[1]))
            for point in bbox
        ]

        cv2.polylines(
            annotated,
            [__import__("numpy").array(points)],
            True,
            (0, 255, 0),
            2
        )

        x = points[0][0]
        y = points[0][1] - 5

        cv2.putText(
            annotated,
            f"{text} ({confidence:.2f})",
            (x, max(y, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 255, 0),
            1
        )

        print(
            f"{detection_number}. "
            f"'{text}' "
            f"(confidence: {confidence:.3f})"
        )

    output_path = os.path.join(
        OUTPUT_DIR,
        f"failed_{index}_detections.jpg"
    )

    cv2.imwrite(output_path, annotated)

    print(f"\nAnnotated image saved:")
    print(output_path)

print("\n" + "=" * 60)
print("FAILED IMAGE INSPECTION COMPLETE")
print("=" * 60)