from django.test import TestCase, tag
from django.contrib.auth.models import User
from apps.blog.models import Post, Category


class BlogTestCase(TestCase):
    list_url = '/'

    @classmethod
    def setUpTestData(cls):
        admin_credentials = {
            'email': 'admin@localhost.ru',
            'username': 'admin',
            'password': '123456'
        }
        user_credentials = {
            'email': 'user@localhost.ru',
            'username': 'user',
            'password': '123456'
        }
        cls.admin = User.objects.create_superuser(**admin_credentials)
        cls.user = User.objects.create_user(**user_credentials)

        cls.category = Category.objects.create(title='Category')
        cls.post_admin = Post.objects.create(
            title='Post',
            category=cls.category,
            author=cls.admin
        )
        cls.post_user = Post.objects.create(
            title='Post',
            category=cls.category,
            author=cls.user
        )
        cls.post_draft = Post.objects.create(
            title='Draft post',
            category=cls.category,
            author=cls.admin,
            draft=True
        )

    @tag('list', 'anonymous')
    def test_view_post_list_by_anonymous(self):
        """Проверка может ли анонимный пользователь видеть список постов"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post_user, response.context_data['post_list'])
        self.assertIn(self.post_admin, response.context_data['post_list'])
        self.assertNotIn(self.post_draft, response.context_data['post_list'])
        self.assertEqual(Post.objects.filter(draft=False).count(), len(response.context_data['post_list']))

    @tag('list', 'user')
    def test_view_book_list_by_user(self):
        """Проверка может ли авторизованный пользователь видеть список постов"""
        self.client.force_login(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post_user, response.context_data['post_list'])
        self.assertIn(self.post_admin, response.context_data['post_list'])
        self.assertNotIn(self.post_draft, response.context_data['post_list'])
        self.assertEqual(Post.objects.filter(draft=False).count(), len(response.context_data['post_list']))

    @tag('list', 'admin')
    def test_view_book_list_by_admin(self):
        """Проверка может ли авторизованный пользователь видеть список постов"""
        self.client.force_login(self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post_user, response.context_data['post_list'])
        self.assertIn(self.post_admin, response.context_data['post_list'])
        self.assertIn(self.post_draft, response.context_data['post_list'])
        self.assertEqual(Post.objects.count(), len(response.context_data['post_list']))
