import json
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from api.views import *
from api.models import Tag, UserProfile
User = get_user_model()
class LifeHackTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    def test_create_lifehack(self): # this test create a lifehack by user request
        tag = Tag.objects.create(name="test tag")
        data = {
            'title':"testing title",
            'description':"Test desc",
            'tag_ids':[tag.id]
        }
        response = self.client.post('/api/lifehacks/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

class UserProfileTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser2", password="testpassword")
        self.profile = UserProfile.objects.create(user=self.user) # disable signals before use this line
        self.target_user = User.objects.create_user(username="targetuser", password="testpassword")
        self.target_profile = UserProfile.objects.create(user=self.target_user)
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_update_userprofile(self):
        data = {
            "bio":"updated bio"
        }
        response = self.client.put(f'/api/profiles/{self.profile.pk}/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_follow_userprofile(self):
        response = self.client.post(f'/api/profiles/{self.target_profile.id}/follow/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.profile, self.target_profile.followers.all())

    def test_unfollow_user(self):
        # First follow
        self.target_profile.followers.add(self.profile)
        response = self.client.post(f'/api/profiles/{self.target_profile.id}/unfollow/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.user.profile, self.target_profile.followers.all())
    