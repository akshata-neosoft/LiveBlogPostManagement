import hashlib
import hmac
import re
from django.core.mail import send_mail
from django.conf import settings


def hash_string_with_secret_key(message: str, secret_key: str) -> str:
    """
    Hash a string using a secret key with HMAC.

    Args:
    - message (str): The message to be hashed.
    - secret_key (str): The secret key to be used for hashing.

    Returns:
    - str: The resulting HMAC hash as a hexadecimal string.
    """
    # Ensure the secret key is in bytes
    secret_key_bytes = secret_key.encode('utf-8')
    # Ensure the message is in bytes
    message_bytes = message.encode('utf-8')

    # Create the HMAC object using the secret key and SHA256 hashing algorithm
    hmac_obj = hmac.new(secret_key_bytes, message_bytes, hashlib.sha256)

    # Get the HMAC digest in hexadecimal format
    hash_hex = hmac_obj.hexdigest()

    return hash_hex


def validate_email(email: str) -> bool:
    """
    Validate the format of an email address.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email format is valid, False otherwise.
    """
    # Define the regular expression for a valid email address
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Match the email address against the regular expression
    if re.match(email_regex, email):
        return True
    return False


def validate_password(password: str) -> bool:
    """
    Validate the format of a password based on specific criteria.

    Args:
        password (str): The password to be validated.

    Returns:
        bool: True if the password meets all criteria, False otherwise.
    """
    # Check if the password contains at least one uppercase letter
    has_upper = bool(re.search(r'[A-Z]', password))

    # Check if the password contains at least one lowercase letter
    has_lower = bool(re.search(r'[a-z]', password))

    # Check if the password contains at least one number
    has_digit = bool(re.search(r'[0-9]', password))

    # Check if the password contains at least one special character
    has_special = bool(re.search(r'[!@#$%^&*()_+{}\[\]:;"\'<>,.?/~\\|-]', password))

    # Check if the password starts with an uppercase letter
    starts_with_upper = password[0].isupper() if password else False

    # Return True if all criteria are met, False otherwise
    return all([has_upper, has_lower, has_digit, has_special, starts_with_upper])


def send_email(subject, message, recipient_list):
    """
    Send an email using Django's email backend.

    Parameters:
    subject (str): Subject of the email
    message (str): Message body of the email
    recipient_list (list): List of recipient email addresses
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, recipient_list)



