# utils/helpers.py

import re

def validate_roll_number(roll):
    """
    Must be exactly 7 digits.
    """
    return bool(re.fullmatch(r"\d{7}", roll))

def validate_uk_phone(phone):
    """
    Accepts formats like: 07123456789, 02012345678
    Landlines: start with 01 or 02, Mobiles: 07
    """
    return bool(re.fullmatch(r"^(0[1-9]{1}[0-9]{8,9})$", phone))
