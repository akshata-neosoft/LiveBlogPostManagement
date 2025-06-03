from rest_framework_extensions.routers import ExtendedDefaultRouter
from django.urls import path, include

from blogpost_management.views.blogpost_viewset import BlogPostViewSet
from django.urls import re_path

from utils import consumer

# from blogpost_management.views.blogpost_views import BlogPostViewSet

router = ExtendedDefaultRouter(trailing_slash=False)

router.register(r'blog', BlogPostViewSet, basename='blog')

urlpatterns = [
    path('', include(router.urls)),

]

websocket_urlpatterns = [
    re_path(r'ws/live-blogs/$', consumer.BlogPostConsumer.as_asgi()),
]
