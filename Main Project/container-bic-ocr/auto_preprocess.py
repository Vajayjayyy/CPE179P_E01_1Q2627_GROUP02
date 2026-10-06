import cv2
import os


INPUT_PATH = "data/test/detected/auto_bic_candidate_1.jpg"
OUTPUT_PATH = "data/test/detected/auto_bic_enhanced.jpg"


print("=" * 60)
print("AUTOMATIC BIC IMAGE PREPROCESSING")
print("=" * 60)


# Load automatically detected crop
image = cv2.imread(INPUT_PATH)

if image is None:
    print("ERROR: Could not load automatic BIC crop.")
    print(INPUT_PATH)
    exit()


print(f"Input image: {INPUT_PATH}")
print(f"Original size: {image.shape[1]} x {image.shape[0]}")


# --------------------------------------------------
# 1. Upscale
# --------------------------------------------------

scale = 4

upscaled = cv2.resize(
    image,
    None,
    fx=scale,
    fy=scale,
    interpolation=cv2.INTER_CUBIC
)


# --------------------------------------------------
# 2. Convert to grayscale
# --------------------------------------------------

gray = cv2.cvtColor(
    upscaled,
    cv2.COLOR_BGR2GRAY
)


# --------------------------------------------------
# 3. Improve contrast
# --------------------------------------------------

enhanced = cv2.equalizeHist(gray)


# --------------------------------------------------
# 4. Save
# --------------------------------------------------

cv2.imwrite(
    OUTPUT_PATH,
    enhanced
)


print(f"Enhanced image saved:")
print(OUTPUT_PATH)

print(
    f"Enhanced size: "
    f"{enhanced.shape[1]} x {enhanced.shape[0]}"
)

print("\nPreprocessing complete.")