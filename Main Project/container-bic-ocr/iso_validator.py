import re


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
    """
    Calculate the ISO 6346 check digit.
    """

    container_number = container_number.upper().strip()

    # Remove spaces
    container_number = container_number.replace(" ", "")

    # First 10 characters are used to calculate the check digit
    body = container_number[:10]

    total = 0

    for index, character in enumerate(body):
        if character.isalpha():
            value = CHAR_MAP[character]
        else:
            value = int(character)

        weight = 2 ** index
        total += value * weight

    check_digit = (total % 11) % 10

    return check_digit


def validate_container_number(container_number):
    """
    Validate an ISO 6346 container number.
    """

    container_number = container_number.upper().strip()
    container_number = container_number.replace(" ", "")

    # ISO 6346 format:
    # 3 letters + U/J/Z + 6 digits + check digit
    pattern = r"^[A-Z]{3}[UJZ]\d{7}$"

    if not re.match(pattern, container_number):
        return False, "Invalid format"

    calculated_digit = calculate_check_digit(container_number)
    actual_digit = int(container_number[-1])

    if calculated_digit == actual_digit:
        return True, "Valid ISO 6346 container number"
    else:
        return False, (
            f"Invalid check digit "
            f"(calculated: {calculated_digit}, "
            f"actual: {actual_digit})"
        )


# Test container number
container_number = "DAYU6721743"

valid, message = validate_container_number(container_number)

print("=" * 60)
print("ISO 6346 CONTAINER NUMBER VALIDATOR")
print("=" * 60)

print(f"Container number: {container_number}")
print(f"Result: {message}")