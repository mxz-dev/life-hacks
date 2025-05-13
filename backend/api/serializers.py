from rest_framework import serializers
from .models import UserProfile, Tag, LifeHack, Comment
from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}, 'password2':{'write_only': True} }
    def create(self, validated_data):
        if validated_data['password'] == validated_data['password2']: 
            user = User.objects.create_user(username=validated_data['username'],password=validated_data['password'], email=validated_data['email'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])
            return user
        raise serializers.ValidationError("Passwords do not match")

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url','id', 'username','email', 'first_name', 'last_name']

class UserProfileMiniSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user']

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail', lookup_field='pk')
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
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail', lookup_field='pk')
    class Meta:
        model = Comment
        fields = ['id', 'user', 'hack', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    