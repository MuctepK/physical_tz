from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from api.views import PostViewSet

default_router = DefaultRouter()

default_router.register('posts', PostViewSet)

urlpatterns = [
    re_path('', include(default_router.urls))
]
