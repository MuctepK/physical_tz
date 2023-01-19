from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from api.views import PostViewSet

default_router = DefaultRouter()

default_router.register(r'posts', PostViewSet)

urlpatterns = [
    re_path('', include(default_router.urls))
]

