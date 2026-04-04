from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=[('technician', 'Technician'), ('physician', 'Physician'), ('admin', 'Admin')])

    def validate_email(self, value):
        from apps.users.models import User
        if User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("An active user with this email already exists.")
        return value

class ConfirmSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6, max_length=6)

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only digits.")
        return value

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        from apps.users.models import User
        user = User.objects.filter(email=value, is_active=False).first()
        if not user:
            raise serializers.ValidationError("No pending verification found for this email.")
        return value

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The base token obtain pair serializer uses authenticate()
        # which respects the user being active or not.
        data = super().validate(attrs)
        
        # Add extra custom claims here if needed
        data['user_id'] = str(self.user.id)
        data['email'] = self.user.email
        data['role'] = self.user.role
        
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Unable to log in with provided credentials.", code="authorization")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.", code="authorization")

        data['user'] = user
        return data
