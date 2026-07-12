from django.core.validators import RegexValidator

PASSWORD_VALIDATOR = RegexValidator(
    regex = r"^\S{8,}$",
    message="Password must contain at least 8 characters and no spaces"
)