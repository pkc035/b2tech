import re
from rest_framework.exceptions import ValidationError

def validate_phone_number(value):
    phone_regex = re.compile(r'^\+?1?\d{9,15}$')
    if not phone_regex.match(value):
        raise ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
