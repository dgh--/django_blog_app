from django.test import TestCase
from django.test import Client

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.shortcuts import reverse

from .models import Comment
from .models import Post
from .utilities import remove_html


class PostModelTests(TestCase):

    def setUp(self):
        Post.objects.create(title = 'Test title.', body = 'Test body.')


class CommentModelTests(TestCase):

    def setUp(self):
        post = Post(title = 'Test Post.', body = 'Test body.')
        post.save()
        post.comments.create(author = 'Test Author', text = 'Test text.')

    def test_comment_should_possess_a_valid_post(self):
        """Each comment should belong to a single specific post."""
        comment = Comment.objects.first()
        post1 = Post.objects.first()
        post2 = comment.post

        self.assertEqual(post1.pk, post2.pk)


class AuthTest(TestCase):

    def setUp(self):
        Post.objects.create(title = 'Test post', body = 'Test body')
        User.objects.create_user(
            username = 'Testuser', 
            password = 'Testpass1', 
            is_staff = True
        )

    def test_staff_user_can_create_and_delete_posts(self):
        """Staff-level users should be able to create and delete posts."""        
        c = Client()
        c.login(username = 'Testuser', password = 'Testpass1')   
        response = c.get(reverse('blog:index'))
        print response
        self.assertContains(response, '<h2>Create a new post</h2>')
        self.assertContains(response, '<a href=\'/1/delete_post/\'> Delete</a>')

    def test_visitors_cannot_create_or_delete_posts(self):
        """None users should not be able to create or delete posts."""
        c = Client()
        response = c.get(reverse('blog:index'))
        print response
        self.assertNotContains(response, '<h2>Create a new post</h2>')
        self.assertNotContains(response, '<a href=\'/1/delete_post/\'> Delete</a>')


class UtilitiesTest(TestCase):

    def test_remove_html_should_remove_any_html(self):
        """HTML tags and their contents should be removed."""
        self.assertEqual(
            remove_html('<a href="/">text</a>'), 
            ''
        )
        self.assertEqual(
            remove_html('<script type="text/javascript">doEvil()</script>'), 
            ''
        )
        
