from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from api.models import LifeHack
from api.serializers import LifeHackSerializer, UserSerializer

User = get_user_model()
class LifeHackViewSet(ModelViewSet):
    """
    A viewset for CRUD on life hacks.
    """
    queryset = LifeHack.objects.all()
    serializer_class = LifeHackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    