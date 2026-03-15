from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from common.responses import success_response
from .serializers import SignupSerializer, ConfirmSignupSerializer, LoginSerializer
from .services import create_user_with_otp, verify_signup_otp


class SignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        create_user_with_otp(email, password)
        return success_response(
            message="Signup successful. Verification OTP sent to email.",
            status_code=status.HTTP_201_CREATED
        )


class ConfirmSignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ConfirmSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp']
        
        user = verify_signup_otp(email, otp_code)
        return success_response(
            message="Account activated successfully. You can now login.",
            status_code=status.HTTP_200_OK
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return success_response(
            data={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                }
            },
            message="Login successful.",
            status_code=status.HTTP_200_OK
        )
