from django.test import TestCase
from .models import Post
from Accounts.models import User


class PostModelTest(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user('Tester', 'tester@gmail.com', 'password')
        self.test_post = Post.objects.create(author=self.test_user, subject='Test', text='This is test')

    def test_like(self):
        post = Post.objects.first()
        post.liked_by.add(self.test_user)
        self.assertTrue(post.is_already_liked(self.test_user))
        self.assertEqual(1, post.likes)