from django.test import TestCase
from django.contrib.auth import get_user_model
from api.models import UserProfile, Comment, LifeHack, Tag

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.profile = UserProfile.objects.create(user=self.user)

    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertTrue(self.profile.user.check_password('testpassword'))
        
class LifeHackModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.tag = Tag.objects.create(name='TestTag')
        self.lifehack = LifeHack.objects.create(
            author = self.user,
            title = 'Test LifeHack',
            description = 'This is a test lifehack.',
        )
        self.lifehack.tag.set([self.tag])
        self.comment = Comment.objects.create(
            user=self.user,
            hack=self.lifehack,
            content='This is a test comment.'
        )

    def test_lifehack_creation(self):
        self.assertEqual(self.lifehack.title, 'Test LifeHack')
        self.assertEqual(self.lifehack.description, 'This is a test lifehack.')
        self.assertEqual(self.lifehack.author.username, 'testuser')
        self.assertEqual(self.lifehack.tag.first().name, 'TestTag')
    
    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'This is a test comment.')
        self.assertEqual(self.comment.user.username, 'testuser')
        self.assertEqual(self.comment.hack.title, 'Test LifeHack')
        