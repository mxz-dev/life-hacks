from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LifeHackViewSet, UserViewSet

router = DefaultRouter()
router.register(r'lifehacks', LifeHackViewSet, basename='lifehack')
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls))
]
