from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from api.models import LifeHack
from api.serializers import LifeHackSerializer, UserSerializer
from api.permissions import IsOwnerOrReadOnly

User = get_user_model()
class LifeHackViewSet(ModelViewSet):
    """
        A viewset for CRUD on life hacks.
    """
    queryset = LifeHack.objects.all()
    serializer_class = LifeHackSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

class UserProfileViewSet():
    pass