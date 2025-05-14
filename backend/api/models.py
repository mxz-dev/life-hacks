from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_query_name="following_user",
        related_name="following_set",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"


class LifeHack(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lifehacks")
    tag = models.ManyToManyField(
        Tag, related_name="tagged_lifehacks", blank=True, null=True
    )
    likes = models.ManyToManyField(User, related_name="liked_hack", blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    hack = models.ForeignKey(
        LifeHack, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.hack.title}"
