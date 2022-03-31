from django.test import TestCase
from .models import Post

class PostTestCases(TestCase):
    def test_get_retrieval(self):
        Post.objects.create(user_id="IAJDIAWKFAO", post_id="DWADAWDAD", postText="My first post!")
        Post.objects.create(user_id="AWDAWASFAW", post_id="26q2aa263a2", postText="My second post!")
        first_post = Post.objects.get(post_id = "DWADAWDAD")
        second_post = Post.objects.get(post_id="26q2aa263a2")
        self.assertEqual(first_post.postText, "My first post!")
        self.assertEqual(second_post.postText, "My second post!")