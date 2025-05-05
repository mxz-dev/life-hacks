from django.contrib.auth import get_user_model
from api.models import UserProfile, Tag, LifeHack, Comment
from api.serializers import UserProfileSerializer, CommentSerializer, LifeHackSerializer
from rest_framework.test import APITestCase

User = get_user_model()
class LifeHackSerializerTestCase(APITestCase):
    def setUp(self):
        # Create a user and a tag for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.tag1 = Tag.objects.create(name='testtag1')
        self.tag2 = Tag.objects.create(name='testtag2')

    def test_valid_serializer_data(self):
        data = {
            'title': 'Test Life Hack',
            'description': 'This is a test life hack.',
            'tag_ids': [self.tag1.id, self.tag2.id],
        }
        self.serializer = LifeHackSerializer(data=data)
        self.assertTrue(self.serializer.is_valid(), "Serializer should be valid")
    def test_serializer_save(self):
        data = {
            "title": "Focus Tip",
            "description": "Block distractions.",
            "tag_ids": [self.tag1.id]
        }
        serializer = LifeHackSerializer(data=data)
        self.assertTrue(serializer.is_valid(), "Serializer should be valid")
        lifehack = serializer.save(author=self.user)
        self.assertEqual(lifehack.title, data['title'])
        self.assertEqual(lifehack.description, data['description'])
        self.assertEqual(lifehack.tag.first().name, self.tag1.name)

    def test_serializer_missing_title(self):
        data = {
            'description': 'This is',
            'tag_ids': [self.tag1.id, self.tag2.id]
        }
        serializer = LifeHackSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

class UserProfileSerializerTest(APITestCase):

    def setUp(self):
        self.user_a = User.objects.create_user(username="user_a", email="a@example.com", password="pass")
        self.user_b = User.objects.create_user(username="user_b", email="b@example.com", password="pass")
        self.user_c = User.objects.create_user(username="user_c", email="c@example.com", password="pass")

        self.profile_a = UserProfile.objects.create(user=self.user_a, bio="Hello, I’m A")
        self.profile_b = UserProfile.objects.create(user=self.user_b)
        self.profile_c = UserProfile.objects.create(user=self.user_c)

        # user_b and user_c follow user_a
        self.profile_a.followers.set([self.profile_b, self.profile_c])
        # user_a follows user_b
        self.profile_a.following_set.set([self.profile_b])

    def test_user_profile_serialization(self):
        serializer = UserProfileSerializer(instance=self.profile_a)

        self.assertEqual(serializer.data['user']['username'], "user_a")
        self.assertEqual(len(serializer.data['followers']), 2)
        self.assertEqual(serializer.data['followers'][0]['user']["username"], "user_b")
        self.assertEqual(len(serializer.data['following_set']), 1)
        self.assertEqual(serializer.data['following_set'][0]['user']['username'], "user_b")

class CommentSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@gmail.com", password="testpassword")
        self.lifehack = LifeHack.objects.create(
            author=self.user,
            title="Test Life Hack",
            description="This is a test life hack."
        )
        self.comment = Comment.objects.create(
            user=self.user,
            hack=self.lifehack,
            content="This is a test comment."
        )
    def test_comment_serialization(self):
        serializer = CommentSerializer(instance=self.comment)
        self.assertEqual(serializer.data['user']['username'], "testuser")
        self.assertEqual(serializer.data['hack'], self.lifehack.id)
        self.assertEqual(serializer.data['content'], "This is a test comment.")
        self.assertIn('created_at', serializer.data)