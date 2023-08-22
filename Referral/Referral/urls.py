from django.contrib import admin
from django.urls import path

from main.views import OTPVerificationView, PhoneAuthorizationView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('authorize-phone/', PhoneAuthorizationView.as_view(), name='phone-authorization'),
    path('verify-otp/', OTPVerificationView.as_view(), name='otp-verification'),
]

