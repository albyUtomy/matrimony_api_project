import re
from django.core.exceptions import ValidationError


def password_validate(password):
    min_len = 8
    max_len = 16

    if len(password) < min_len or len(password) > max_len:
        raise ValidationError("Password must be between 8 and 16 characters long")
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase")
    
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase")
    
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*()_\-+=\[\]{}|;:,.<>?/]', password):
        raise ValidationError("Password should contain at least one special character")    
    return password


def validate_phone_number(value):
    # regular expression to validate the phone number
    pattern = r'^[6-9]\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError("Invalid phone number.")
    
