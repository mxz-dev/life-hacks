from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LifeHackViewSet, UserViewSet, UserProfileViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'lifehacks', LifeHackViewSet, basename='lifehack')
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls))
]
