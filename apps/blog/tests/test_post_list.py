from django.test import TestCase, tag
from django.contrib.auth.models import User
from apps.blog.models import Post, Category


def create_user(username: str = "user") -> User:
    return User.objects.create_user(username=username, email=f"{username}@example.com", password="123456")


class BlogPostListTestCase(TestCase):
    url = '/'

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user()
        cls.another_user = create_user(username="another_user")

        cls.category = Category.objects.create(title='Category')
        cls.user_post = Post.objects.create(title='Post 1', category=cls.category, author=cls.user)
        cls.another_user_post = Post.objects.create(title='Post 2', category=cls.category, author=cls.another_user)
        cls.another_user_post_draft = Post.objects.create(
            title='Draft post', category=cls.category, author=cls.another_user, draft=True
        )

    @tag('list', 'anonymous')
    def test_view_post_list_by_anonymous(self):
        """Проверка может ли анонимный пользователь видеть список постов."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_post, response.context_data['post_list'])
        self.assertIn(self.another_user_post, response.context_data['post_list'])
        self.assertNotIn(self.another_user_post_draft, response.context_data['post_list'])
        self.assertEqual(Post.objects.filter(draft=False).count(), len(response.context_data['post_list']))

    @tag('list', 'user')
    def test_view_post_list_by_user(self):
        """Проверка может ли авторизованный пользователь видеть список постов."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_post, response.context_data['post_list'])
        self.assertIn(self.another_user_post, response.context_data['post_list'])
        self.assertNotIn(self.another_user_post_draft, response.context_data['post_list'])
        self.assertEqual(Post.objects.filter(draft=False).count(), len(response.context_data['post_list']))

    @tag('list', 'another_user')
    def test_view_post_list_by_another_user(self):
        """Проверка может ли авторизованный пользователь видеть список постов, в том числе с черновиками."""
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_post, response.context_data['post_list'])
        self.assertIn(self.another_user_post, response.context_data['post_list'])
        self.assertIn(self.another_user_post_draft, response.context_data['post_list'])
        self.assertEqual(Post.objects.count(), len(response.context_data['post_list']))
