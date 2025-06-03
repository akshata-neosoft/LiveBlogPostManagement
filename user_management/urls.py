from rest_framework_extensions.routers import ExtendedDefaultRouter
from django.urls import path, include

from user_management.views.login_viewset import LoginViewSet

router = ExtendedDefaultRouter(trailing_slash=False)

router.register(r'user', LoginViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]