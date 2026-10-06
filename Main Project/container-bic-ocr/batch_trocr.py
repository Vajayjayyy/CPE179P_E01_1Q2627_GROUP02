from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import os

CROP_DIR = "data/test/batch_enhanced"

IMAGE_FILES = [
    "image_2_candidate_enhanced.jpg",
    "image_4_candidate_enhanced.jpg",
    "image_5_candidate_enhanced.jpg",
]

print("=" * 60)
print("BATCH TROCR TEST")
print("=" * 60)

print("\nLoading TrOCR...")

processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-base-printed"
)

model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-printed"
)

print("TrOCR loaded.")

for index, filename in enumerate(IMAGE_FILES, start=1):

    image_path = os.path.join(CROP_DIR, filename)

    print("\n" + "=" * 60)
    print(f"IMAGE {index}: {filename}")
    print("=" * 60)

    image = Image.open(image_path).convert("RGB")

    pixel_values = processor(
        images=image,
        return_tensors="pt"
    ).pixel_values

    generated_ids = model.generate(
        pixel_values,
        max_new_tokens=20
    )

    result = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    print(f"TrOCR result: {result}")

print("\n" + "=" * 60)
print("BATCH TROCR TEST COMPLETE")
print("=" * 60)