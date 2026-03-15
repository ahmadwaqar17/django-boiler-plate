from django.urls import path
from .views import SignupView, ConfirmSignupView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('confirm-signup/', ConfirmSignupView.as_view(), name='confirm_signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
