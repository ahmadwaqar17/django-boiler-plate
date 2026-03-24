from rest_framework.exceptions import APIException
from rest_framework import status

class BaseCustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A custom API error occurred.'
    default_code = 'custom_error'

class UserNotFoundException(BaseCustomException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'The requested user could not be found.'
    default_code = 'user_not_found'

class OTPVerificationException(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'OTP verification failed due to invalid codes or limits.'
    default_code = 'otp_verification_failed'
