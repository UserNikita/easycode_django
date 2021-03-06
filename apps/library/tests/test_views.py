from django.test import TestCase, tag
from django.contrib.auth.models import User
from apps.library.models import Book


class LibraryTestCase(TestCase):
    list_url = '/library/'
    detail_url = '/library/book/{id}/'
    create_url = '/library/book/add/'

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

        cls.book = Book.objects.create(
            title='Book title',
            description='Description',
            year=2018,
            url='http://example.com/book/1/',
            size=2.5,
        )

    @tag('list', 'anonymous')
    def test_view_book_list_by_anonymous(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.book.id, response.context_data['book_list'][0].id)
        self.assertEqual(self.book.title, response.context_data['book_list'][0].title)
        self.assertEqual(Book.objects.count(), len(response.context_data['book_list']))

    @tag('list', 'user')
    def test_view_book_list_by_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.book.id, response.context_data['book_list'][0].id)
        self.assertEqual(self.book.title, response.context_data['book_list'][0].title)
        self.assertEqual(Book.objects.count(), len(response.context_data['book_list']))

    @tag('list', 'admin')
    def test_view_book_list_by_admin(self):
        self.client.force_login(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.book.id, response.context_data['book_list'][0].id)
        self.assertEqual(self.book.title, response.context_data['book_list'][0].title)
        self.assertEqual(Book.objects.count(), len(response.context_data['book_list']))

    def test_book_list_filtered_by_anonymous(self):
        response = self.client.get(self.list_url, {'title': 'Book'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), len(response.context_data['book_list']))

    def test_book_list_case_insensitive_filtered_by_anonymous(self):
        response = self.client.get(self.list_url, {'title': 'book'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), len(response.context_data['book_list']))
