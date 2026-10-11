from functools import lru_cache
from pathlib import Path
import re

import cv2
import easyocr
import numpy as np
from PIL import Image
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

MODEL_NAME = "microsoft/trocr-base-printed"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

@lru_cache(maxsize=1)
def get_models():
    """Load the OCR models once per application process."""
    reader = easyocr.Reader(["en"], gpu=(DEVICE == "cuda"))
    processor = TrOCRProcessor.from_pretrained(MODEL_NAME)
    model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME).to(DEVICE)
    model.eval()
    return reader, processor, model

def _trocr_read(image: Image.Image, processor, model) -> str:
    image = image.convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(DEVICE)
    with torch.inference_mode():
        generated = model.generate(pixel_values, max_new_tokens=32)
    return processor.batch_decode(generated, skip_special_tokens=True)[0].strip()

def _clean_code_text(value: str) -> str:
    value = value.upper().replace(" ", "").replace("-", "").replace("_", "")
    # Common OCR confusions in numeric positions.
    if len(value) >= 11 and value[:4].isalpha():
        prefix = value[:4]
        digits = value[4:11].translate(str.maketrans({
            "O": "0", "Q": "0", "D": "0",
            "I": "1", "L": "1", "S": "5", "B": "8", "Z": "2"
        }))
        return prefix + digits
    return value

def _extract_candidates(texts):
    candidates = []
    seen = set()
    for text in texts:
        compact = re.sub(r"[^A-Z0-9]", "", text.upper())
        # Search windows because OCR may return surrounding labels too.
        for match in re.finditer(r"[A-Z]{4}[A-Z0-9]{7}", compact):
            raw = match.group(0)
            code = _clean_code_text(raw)
            if re.fullmatch(r"[A-Z]{4}\d{7}", code) and code not in seen:
                seen.add(code)
                candidates.append(code)
        # Handle spaces between prefix, serial number, and check digit.
        separated = re.sub(r"[^A-Z0-9]", " ", text.upper())
        for match in re.finditer(r"([A-Z]{4})\s*([0-9OQDI LSBZ]{6,7})", separated):
            code = _clean_code_text(match.group(1) + match.group(2))
            if re.fullmatch(r"[A-Z]{4}\d{7}", code) and code not in seen:
                seen.add(code)
                candidates.append(code)
    return candidates

def process_image(image_bytes: bytes, filename: str = "uploaded-image") -> dict:
    """Run EasyOCR detection and TrOCR recognition; return JSON-safe data."""
    import io
    try:
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise ValueError("The uploaded file is not a readable image.") from exc

    if pil_image.width < 32 or pil_image.height < 32:
        raise ValueError("Image is too small. Please upload a clearer image.")

    reader, processor, model = get_models()
    cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    detections = reader.readtext(cv_image, detail=1, paragraph=False)
    detected_texts = []
    detection_details = []
    for box, text, confidence in detections:
        text = str(text).strip()
        if text:
            detected_texts.append(text)
            detection_details.append({
                "text": text,
                "confidence": round(float(confidence), 4),
                "box": [[int(p[0]), int(p[1])] for p in box]
            })

    # Full-image TrOCR is useful for images where the container code is prominent.
    trocr_text = _trocr_read(pil_image, processor, model)
    all_texts = [trocr_text] + detected_texts
    candidates = _extract_candidates(all_texts)

    # Also recognize individual EasyOCR regions with TrOCR. This helps when the
    # whole image contains clutter, while keeping the original image intact.
    h, w = cv_image.shape[:2]
    for item in detection_details[:12]:
        points = item["box"]
        x1 = max(0, min(p[0] for p in points) - 8)
        y1 = max(0, min(p[1] for p in points) - 8)
        x2 = min(w, max(p[0] for p in points) + 8)
        y2 = min(h, max(p[1] for p in points) + 8)
        if x2 - x1 < 8 or y2 - y1 < 8:
            continue
        crop = Image.fromarray(cv2.cvtColor(cv_image[y1:y2, x1:x2], cv2.COLOR_BGR2RGB))
        try:
            crop_text = _trocr_read(crop, processor, model)
            if crop_text:
                all_texts.append(crop_text)
        except Exception:
            pass

    candidates = _extract_candidates(all_texts)
    from validation import validate_container_code
    checked = []
    for code in candidates:
        result = validate_container_code(code)
        checked.append({"code": code, **result})

    valid_codes = [item for item in checked if item["valid"]]
    best = valid_codes[0] if valid_codes else (checked[0] if checked else None)

    return {
        "filename": Path(filename).name,
        "recognized_code": best["code"] if best else None,
        "iso6346_valid": bool(best["valid"]) if best else False,
        "check_digit_valid": bool(best["check_digit_valid"]) if best else False,
        "candidates": checked,
        "trocr_full_image_text": trocr_text,
        "easyocr_text": detected_texts,
        "detections": detection_details,
        "message": (
            "Valid ISO 6346 code candidate found."
            if valid_codes else
            "Text detected, but no valid ISO 6346 code was confirmed. Review the candidates or try a clearer image."
            if checked else
            "No complete container code was detected. Try a sharper, closer image with the code clearly visible."
        )
    }
