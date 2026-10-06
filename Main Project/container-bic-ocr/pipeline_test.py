import re
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel


IMAGE_PATH = "data/test/detected/container_id_enhanced.jpg"


# ISO 6346 character values
CHAR_MAP = {
    "A": 10, "B": 12, "C": 13, "D": 14, "E": 15,
    "F": 16, "G": 17, "H": 18, "I": 19, "J": 20,
    "K": 21, "L": 23, "M": 24, "N": 25, "O": 26,
    "P": 27, "Q": 28, "R": 29, "S": 30, "T": 31,
    "U": 32, "V": 34, "W": 35, "X": 36, "Y": 37,
    "Z": 38
}


def calculate_check_digit(container_number):

    body = container_number[:10]

    total = 0

    for index, character in enumerate(body):

        if character.isalpha():
            value = CHAR_MAP[character]
        else:
            value = int(character)

        total += value * (2 ** index)

    return (total % 11) % 10


def validate_container_number(container_number):

    container_number = container_number.upper()
    container_number = container_number.replace(" ", "")

    pattern = r"^[A-Z]{3}[UJZ]\d{7}$"

    if not re.match(pattern, container_number):
        return False, "Invalid format"

    calculated = calculate_check_digit(container_number)
    actual = int(container_number[-1])

    if calculated == actual:
        return True, "VALID ISO 6346"

    return False, (
        f"INVALID CHECK DIGIT "
        f"(calculated {calculated}, actual {actual})"
    )


print("=" * 60)
print("CONTAINER BIC OCR - COMPLETE PIPELINE TEST")
print("=" * 60)


# --------------------------------------------------
# STEP 1: LOAD TrOCR
# --------------------------------------------------

print("\n[1/3] Loading TrOCR...")

processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-base-printed"
)

model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-printed"
)

print("TrOCR loaded.")


# --------------------------------------------------
# STEP 2: OCR
# --------------------------------------------------

print("\n[2/3] Reading container ID...")

image = Image.open(IMAGE_PATH).convert("RGB")

pixel_values = processor(
    images=image,
    return_tensors="pt"
).pixel_values

generated_ids = model.generate(
    pixel_values,
    max_new_tokens=20
)

ocr_text = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True
)[0]

print(f"Raw TrOCR result: {ocr_text}")


# --------------------------------------------------
# STEP 3: CLEAN OCR RESULT
# --------------------------------------------------

cleaned = ocr_text.upper()

cleaned = re.sub(
    r"[^A-Z0-9]",
    "",
    cleaned
)

print(f"Cleaned result:    {cleaned}")


# --------------------------------------------------
# STEP 4: ISO VALIDATION
# --------------------------------------------------

print("\n[3/3] Validating ISO 6346...")

valid, message = validate_container_number(cleaned)

print(f"Container ID: {cleaned}")
print(f"Validation:   {message}")


print("\n" + "=" * 60)

if valid:
    print("FINAL RESULT: VERIFIED CONTAINER")
else:
    print("FINAL RESULT: NOT VERIFIED")

print("=" * 60)