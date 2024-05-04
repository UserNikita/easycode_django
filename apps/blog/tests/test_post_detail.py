from django.test import TestCase, tag
from django.contrib.auth.models import User

from apps.blog.models import Post, Category


def create_user(username: str = "user") -> User:
    return User.objects.create_user(username=username, email=f"{username}@example.com", password="123456")


class BlogPostDetailTestCase(TestCase):
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

    @tag('detail', 'anonymous')
    def test_view_post_detail_by_anonymous(self):
        """Проверка может ли анонимный пользователь видеть пост."""
        post = self.user_post
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post, response.context_data['post'])

        post = self.another_user_post
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post, response.context_data['post'])

        post = self.another_user_post_draft
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 302)  # Аноним не видит черновики

    @tag('detail', 'user')
    def test_view_post_detail_by_user(self):
        """Проверка может ли авторизованный пользователь видеть пост."""
        self.client.force_login(self.user)

        post = self.user_post
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post, response.context_data['post'])

        post = self.another_user_post
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post, response.context_data['post'])

        post = self.another_user_post_draft
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 403)  # Пользователь не видит черновик другого пользователя

    @tag('detail', 'another_user')
    def test_view_post_detail_by_another_user(self):
        """Проверка может ли авторизованный пользователь видеть свой черновой пост."""
        self.client.force_login(self.another_user)

        post = self.user_post
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post, response.context_data['post'])

        post = self.another_user_post
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post, response.context_data['post'])

        post = self.another_user_post_draft
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)  # Пользователь видит свой черновик
