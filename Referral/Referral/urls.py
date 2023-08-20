from django.contrib import admin
from django.urls import path

from main.views import UserRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
