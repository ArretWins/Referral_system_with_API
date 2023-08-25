from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import PhoneAuthorizationView, PhoneLoginView, UserViewSet, UserProfileViewSet, LogoutView


router = DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'users', UserProfileViewSet)
router.register(r'user-profile', UserProfileViewSet, basename='user-profile')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('send-otp/', PhoneAuthorizationView.as_view(), name='send-otp'),
    path('login/', PhoneLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileViewSet.as_view({'post': 'activate_invite_code'}), name='profile'),
    path('', include(router.urls)),  # Включаем роутер URL-путей
    path('api/', include(router.urls)),
    # path('activate-invite-code/', UserProfileViewSet.as_view({'post': 'activate_invite_code'}), name='activate_invite_code'),
]

