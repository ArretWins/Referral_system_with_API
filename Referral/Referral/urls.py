from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import PhoneAuthorizationView, PhoneLoginView, UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('send-otp/', PhoneAuthorizationView.as_view(), name='send-otp'),
    path('login/', PhoneLoginView.as_view(), name='login'),
    path('', include(router.urls)),  # Включаем роутер URL-путей
]

