import cv2
import os

INPUT_DIR = "data/test/batch_candidates_v2"
OUTPUT_DIR = "data/test/batch_enhanced"

IMAGE_FILES = [
    "image_2_candidate.jpg",
    "image_4_candidate.jpg",
    "image_5_candidate.jpg",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("BATCH IMAGE PREPROCESSING")
print("=" * 60)

for filename in IMAGE_FILES:

    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(
        OUTPUT_DIR,
        filename.replace(".jpg", "_enhanced.jpg")
    )

    image = cv2.imread(input_path)

    if image is None:
        print(f"\nERROR: Could not load {filename}")
        continue

    # Upscale 4x
    enlarged = cv2.resize(
        image,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC
    )

    # Convert to grayscale
    gray = cv2.cvtColor(
        enlarged,
        cv2.COLOR_BGR2GRAY
    )

    # Improve contrast
    enhanced = cv2.equalizeHist(gray)

    cv2.imwrite(output_path, enhanced)

    print(f"\nProcessed: {filename}")
    print(f"Saved: {output_path}")

print("\n" + "=" * 60)
print("PREPROCESSING COMPLETE")
print("=" * 60)