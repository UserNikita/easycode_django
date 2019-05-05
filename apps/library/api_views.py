from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Category, Book
from .serializers import CategorySerializer, BookSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
