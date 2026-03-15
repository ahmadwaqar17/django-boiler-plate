import secrets
import string

def generate_random_otp(length=6):
    """Generates a random numerical OTP of specified length."""
    return ''.join(secrets.choice(string.digits) for i in range(length))
