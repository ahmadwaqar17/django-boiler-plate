from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import User, OTP
from common.utils import generate_random_otp
from common.constants import OTP_EXPIRATION_MINUTES, MAX_OTP_ATTEMPTS


def get_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

def create_user_with_otp(email, password):
    """Creates a new inactive user and generates an OTP for signup."""
    
    # Check if user already exists
    user = get_user_by_email(email)
    
    if user:
        if user.is_active:
            # OTP generation when user already verified.
            raise ValueError("User with this email already exists and is active.")
        else:
            # User exists but is inactive, perhaps tried to signup before.
            # We can update the password and send a new OTP.
            user.set_password(password)
            user.save()
    else:
        # Create new inactive user
        user = User.objects.create_user(email=email, password=password)
        user.is_active = False
        user.save()

    # Generate and send OTP (this also invalidates previous active OTPs)
    otp_obj = generate_otp(email, purpose='signup')
    send_signup_otp_email(email, otp_obj.otp_code)
    
    return user

def generate_otp(email, purpose='signup'):
    """Generates an OTP for the given email and invalidates old ones."""
    
    # Invalidate existing OTPs for this email and purpose
    OTP.objects.filter(email=email, purpose=purpose, is_used=False).update(is_used=True)
    
    otp_code = generate_random_otp()
    expires_at = timezone.now() + timedelta(minutes=OTP_EXPIRATION_MINUTES)
    
    otp_obj = OTP.objects.create(
        email=email,
        otp_code=otp_code,
        purpose=purpose,
        expires_at=expires_at
    )
    return otp_obj

def send_signup_otp_email(email, otp_code):
    """Sends OTP via standard Django email backend."""
    subject = "Confirm your signup"
    message = f"Your verification code is: {otp_code}. It expires in {OTP_EXPIRATION_MINUTES} minutes."
    
    send_mail(
        subject,
        message,
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
        [email],
        fail_silently=False,
    )

def verify_signup_otp(email, otp_code):
    """Verifies the given OTP and activates the user if valid."""
    # First, fetch the most recent unused OTP for this email and purpose that hasn't exceeded max attempts
    # We fetch it regardless of if the code matches to track bad attempts on the valid OTP session.
    latest_otp = OTP.objects.filter(
        email=email,
        purpose='signup',
        is_used=False
    ).order_by('-created_at').first()

    if not latest_otp:
        raise ValueError("No active OTP request found for this email.")
    
    # Check if the session itself is valid (expired or locked)
    is_valid_state, error_msg = latest_otp.is_valid(max_attempts=MAX_OTP_ATTEMPTS)
    if not is_valid_state:
        raise ValueError(error_msg)

    # Now verify the code
    if latest_otp.otp_code != otp_code:
        # We got a wrong code, increment failed attempts on the active session
        latest_otp.failed_attempts += 1
        latest_otp.save()
        
        # Check if they just hit the max limit
        if latest_otp.failed_attempts >= MAX_OTP_ATTEMPTS:
            raise ValueError(f"Maximum verification attempts exceeded ({MAX_OTP_ATTEMPTS}). Please request a new OTP.")
            
        raise ValueError(f"Invalid OTP. Attempt {latest_otp.failed_attempts} of {MAX_OTP_ATTEMPTS}.")
    
    # Valid OTP (the code matches and session is valid)
    user = get_user_by_email(email)
    if not user:
        raise ValueError("User not found.")
        
    activate_user(user)
    
    # Mark OTP as used
    latest_otp.is_used = True
    latest_otp.save()
    
    # Invalidate all other unused OTPs for safety
    OTP.objects.filter(email=email, purpose='signup', is_used=False).update(is_used=True)
    
    return user

def activate_user(user):
    """Activates a user account."""
    user.is_active = True
    user.is_verified = True
    user.save()
    return user
