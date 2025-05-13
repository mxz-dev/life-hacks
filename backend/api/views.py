from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from api.models import LifeHack, UserProfile, Comment
from api.serializers import (
    LifeHackSerializer,
    UserSerializer,
    UserProfileSerializer,
    CommentSerializer,
    UserRegisterationSerializer,
)
from api.permissions import IsOwnerOrReadOnly, IsProfileOwnerOrReadOnly

User = get_user_model()


class LifeHackViewSet(ModelViewSet):
    """
    A viewset for CRUD on life hacks.
    """

    queryset = LifeHack.objects.all()
    serializer_class = LifeHackSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description", "author__username"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        hack = self.get_object()
        user = request.user
        hack.likes.add(user)
        return Response({"status": "liked"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        hack = self.get_object()
        hack.likes.remove(request.user)
        return Response({"status": "unliked"}, status=status.HTTP_200_OK)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserProfileViewSet(ModelViewSet):  # need to test
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]

    def perform_update(self, serializer):
        # Update the profile with the current logged-in user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"])
    def update_avatar(self, request, pk=None):
        user_profile = self.get_object()
        avatar = request.FILES.get("avatar")
        if avatar:
            user_profile.avatar = avatar
            user_profile.save()
            return Response(
                {"detail": "Avatar updated successfully."}, status=status.HTTP_200_OK
            )
        return Response(
            {"detail": "No avatar provided."}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        target_profile = self.get_object()
        user_profile = request.user.profile
        if target_profile == user_profile:
            return Response(
                {"error": "You can't follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        target_profile.followers.add(user_profile)
        return Response({"success": "Followed successfully!"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        target_profile = self.get_object()
        user_profile = request.user.profile
        if user_profile in target_profile.followers.all():
            target_profile.followers.remove(user_profile)
            return Response(
                {"success": "Unfollowed Successfully!"}, status=status.HTTP_200_OK
            )
        return Response({"error": "You are not following this user."}, status=400)

    def perform_destroy(self, instance):
        return Response(
            {"detail": "You cannot delete your profile."},
            status=status.HTTP_403_FORBIDDEN,
        )


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserRegisterationAPI(GenericAPIView):
    """
    A view for user registration.
    """

    serializer_class = UserRegisterationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": {"id": user.id, "username": user.username, "email": user.email},
            }
        )
