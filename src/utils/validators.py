"""
Validators for input data
"""
import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, "Valid email"
    return False, "Invalid email format"


def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validate phone number"""
    pattern = r'^[\d\s\-\+\(\)]{10,}$'
    if re.match(pattern, phone):
        return True, "Valid phone"
    return False, "Invalid phone format"


def validate_plate_number(plate: str) -> Tuple[bool, str]:
    """Validate vehicle plate number"""
    # Vietnamese plate format
    pattern = r'^[0-9]{2}[A-Z]{1}[-]{1}[0-9]{4,5}$'
    if re.match(pattern, plate):
        return True, "Valid plate"
    return False, "Invalid plate format"


def validate_url(url: str) -> Tuple[bool, str]:
    """Validate URL format"""
    pattern = r'^https?://[^\s]+$'
    if re.match(pattern, url):
        return True, "Valid URL"
    return False, "Invalid URL format"
