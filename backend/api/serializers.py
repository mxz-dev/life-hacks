from rest_framework import serializers
from .models import UserProfile, Tag, LifeHack, Comment
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url','id', 'username']

class UserProfileMiniSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers = UserProfileMiniSerializer(many=True, read_only=True)
    following_set = UserProfileMiniSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'avatar', 'followers', 'following_set']
        read_only_fields = ['id', 'user', 'followers', 'following_set']
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class LifeHackSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail', lookup_field='pk')

    tag = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source='tag', many=True, write_only=True
    )
    class Meta:
        model = LifeHack
        fields = [
            'id',
            'author',
            'title',
            'description',
            'tag',
            'tag_ids',
            'created_at',
            'updated_at',
            ]

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'hack', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
        