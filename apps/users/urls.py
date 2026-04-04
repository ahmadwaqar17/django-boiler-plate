from django.urls import path
from apps.users.views import SignupView, ConfirmSignupView, LoginView, ResendOTPView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('confirm-signup/', ConfirmSignupView.as_view(), name='confirm_signup'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
