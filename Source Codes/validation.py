import re

# ISO 6346 letter values. Values skip multiples of 11.
LETTER_VALUES = {
    "A": 10, "B": 12, "C": 13, "D": 14, "E": 15, "F": 16,
    "G": 17, "H": 18, "I": 19, "J": 20, "K": 21, "L": 23,
    "M": 24, "N": 25, "O": 26, "P": 27, "Q": 28, "R": 29,
    "S": 30, "T": 31, "U": 32, "V": 34, "W": 35, "X": 36,
    "Y": 37, "Z": 38
}

def calculate_check_digit(code10: str):
    """Calculate ISO 6346 check digit for owner/category + six-digit serial."""
    code10 = re.sub(r"[\s-]", "", code10.upper())
    if not re.fullmatch(r"[A-Z]{4}\d{6}", code10):
        raise ValueError("Expected four letters followed by six digits.")
    total = 0
    for position, char in enumerate(code10):
        value = LETTER_VALUES[char] if char.isalpha() else int(char)
        total += value * (2 ** position)
    remainder = total % 11
    return 0 if remainder == 10 else remainder

def validate_container_code(code: str) -> dict:
    normalized = re.sub(r"[\s-]", "", (code or "").upper())
    format_valid = bool(re.fullmatch(r"[A-Z]{4}\d{7}", normalized))
    if not format_valid:
        return {
            "normalized_code": normalized,
            "format_valid": False,
            "check_digit_valid": False,
            "valid": False,
            "expected_check_digit": None,
            "message": "Expected format: 4 letters + 6 serial digits + 1 check digit."
        }
    expected = calculate_check_digit(normalized[:10])
    actual = int(normalized[10])
    check_valid = expected == actual
    return {
        "normalized_code": normalized,
        "format_valid": True,
        "check_digit_valid": check_valid,
        "valid": check_valid,
        "expected_check_digit": expected,
        "message": "Valid ISO 6346 check digit." if check_valid else f"Check digit mismatch: expected {expected}, got {actual}."
    }
