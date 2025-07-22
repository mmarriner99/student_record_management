# utils/helpers.py

import re

def validate_roll_number(roll):
    """
    Must be exactly 7 digits.
    """
    if not roll:
        return False
    roll = str(roll).strip()
    return bool(re.fullmatch(r"\d{7}", roll))

def validate_uk_phone(phone):
    """
    Accepts UK phone number formats:
    - Mobile: 07xxxxxxxxx (11 digits starting with 07)
    - Landline: 01xxxxxxxxx or 02xxxxxxxxx (11 digits starting with 01/02)
    - Also accepts some 10-digit landlines
    """
    if not phone:
        return False
    
    # Remove spaces, hyphens, and other non-digit characters except +
    phone = str(phone).strip()
    
    # Handle +44 format
    if phone.startswith('+44'):
        phone = phone.replace('+44', '0', 1)
    
    # Remove all non-digit characters
    phone = re.sub(r'[^\d]', '', phone)
    
    # Must start with 0 and be 10 or 11 digits
    if not phone.startswith('0'):
        return False
    
    # Check specific patterns
    patterns = [
        r'^0[1-2]\d{8,9}$',  # Landlines: 01xxx or 02xxx (10-11 digits)
        r'^03\d{9}$',        # Non-geographic: 03xxx (11 digits)
        r'^07\d{9}$',        # Mobile: 07xxx (11 digits)
        r'^08\d{9}$',        # Freephone/Special: 08xxx (11 digits)
        r'^09\d{9}$'         # Premium rate: 09xxx (11 digits)
    ]
    
    return any(re.match(pattern, phone) for pattern in patterns)

def format_uk_phone(phone):
    """
    Format UK phone number for consistent display
    """
    if not phone:
        return phone
    
    phone = str(phone).strip()
    
    # Handle +44 format
    if phone.startswith('+44'):
        phone = phone.replace('+44', '0', 1)
    
    # Remove all non-digit characters
    phone = re.sub(r'[^\d]', '', phone)
    
    # Ensure starts with 0
    if phone and not phone.startswith('0') and len(phone) in [10, 11]:
        phone = '0' + phone
    
    return phone

def validate_student_name(name):
    """
    Validate student name - should contain only letters, spaces, hyphens, apostrophes
    """
    if not name or not name.strip():
        return False
    
    name = name.strip()
    
    # Must be at least 2 characters and not more than 50
    if len(name) < 2 or len(name) > 50:
        return False
    
    # Should contain only letters, spaces, hyphens, and apostrophes
    pattern = r"^[a-zA-Z\s\-']+$"
    return bool(re.match(pattern, name))

def sanitize_input(text, max_length=None):
    """
    Basic input sanitization
    """
    if not text:
        return ""
    
    text = str(text).strip()
    
    if max_length:
        text = text[:max_length]
    
    return text