from django.test import TestCase
from django.contrib.auth.models import User, Permission


class LibraryTestCase(TestCase):
    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        cls.admin_credentials = {
            'email': 'admin@localhost.ru',
            'username': 'admin',
            'password': '123456'
        }
        cls.user_credentials = {
            'email': 'user@localhost.ru',
            'username': 'user',
            'password': '123456'
        }
        User.objects.create_superuser(**cls.admin_credentials)
        User.objects.create_user(**cls.user_credentials)

    def test_book_list(self):
        """Проверка возможности просматривать список книг"""
        url = '/library/'

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        self.client.login(**self.user_credentials)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        self.client.login(**self.admin_credentials)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_book_add(self):
        """Проверка возможности добавлять книги в библиотеку"""
        url = '/library/book/add/'

        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

        self.client.login(**self.user_credentials)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

        self.client.login(**self.admin_credentials)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
