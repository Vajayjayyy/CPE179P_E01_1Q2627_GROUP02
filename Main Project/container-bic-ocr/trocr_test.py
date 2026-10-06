from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

IMAGE_PATH = "data/test/detected/auto_bic_enhanced.jpg"

print("=" * 60)
print("CONTAINER BIC OCR - TrOCR TEST")
print("=" * 60)

print("\nLoading TrOCR model...")

processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-base-printed"
)

model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-printed"
)

print("TrOCR loaded.")

print("\nLoading container ID crop...")

image = Image.open(IMAGE_PATH).convert("RGB")

print(f"Image loaded: {IMAGE_PATH}")

# Prepare image for TrOCR
pixel_values = processor(
    images=image,
    return_tensors="pt"
).pixel_values

# Generate text
print("\nRecognizing text...")

generated_ids = model.generate(pixel_values)

text = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True
)[0]

print("\n========================================")
print("TrOCR RESULT:")
print(text)
print("========================================")