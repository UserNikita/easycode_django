from rest_framework.serializers import ModelSerializer

from .models import Category, Book


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
