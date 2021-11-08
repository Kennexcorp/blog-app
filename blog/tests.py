from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from blog.models import Post


class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='kennexcorp',
            email='ekeneoguikpu@gmail.com',
            password='secret'
        )

        self.post = Post.objects.create(
            title='A new test',
            body='A test body',
            author=self.user,
        )
    def test_string_representation(self):
        post = Post(title='A test sample')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A new test')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A test body')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)

    def test_post_create_view(self):  # new
        response = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New text',
            'author': self.user.id,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'New title')
        self.assertEqual(Post.objects.last().body, 'New text')

    def test_post_update_view(self):  # new
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated title',
            'body': 'Updated text',
        })

        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):  # new
        response = self.client.post(
            reverse('post_delete', args='1'))

        self.assertEqual(response.status_code, 302)