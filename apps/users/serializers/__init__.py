from .auth import SignupSerializer, ConfirmSignupSerializer, CustomTokenObtainPairSerializer, LoginSerializer, ResendOTPSerializer, LogoutSerializer
from .profile import PhysicianProfileSerializer

__all__ = [
    'SignupSerializer', 'ConfirmSignupSerializer', 'CustomTokenObtainPairSerializer', 
    'LoginSerializer', 'ResendOTPSerializer', 'LogoutSerializer',
    'PhysicianProfileSerializer'
]

