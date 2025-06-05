from rest_framework_extensions.routers import ExtendedDefaultRouter
from django.urls import path, include

from user_management.views.login_viewset import LoginViewSet
from user_management.views.profile_viewset import ProfileViewSet

router = ExtendedDefaultRouter(trailing_slash=False)

router.register(r'user', LoginViewSet, basename='user')
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]