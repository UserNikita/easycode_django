from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django_filters.views import FilterMixin
from django.db.models import Max, Min, Avg, Sum

from apps.personal_area.forms import CommentForm
from apps.personal_area.models import Comment
from .filtersets import BookFilterSet
from .models import *
from .forms import *


class BookListView(FilterMixin, ListView):
    template_name = 'library/book_list.html'
    model = Book
    paginate_by = 16
    filterset_class = BookFilterSet

    def get_queryset(self):
        qs = super(BookListView, self).get_queryset().filter(draft=False)
        return qs

    def get_context_data(self, **kwargs):
        filterset = self.get_filterset(self.get_filterset_class())
        kwargs['filter'] = filterset
        kwargs['object_list'] = filterset.qs
        return super().get_context_data(**kwargs)


class TagBookListView(BookListView):
    template_name = 'library/book_list_tag.html'
    category = None

    def get_queryset(self):
        queryset = super(TagBookListView, self).get_queryset()
        self.tag = Tag.objects.get(id=self.kwargs.get('tag'))
        queryset = queryset.filter(tags=self.tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TagBookListView, self).get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class BookDetailView(DetailView, UserPassesTestMixin, ProcessFormView, FormMixin):
    template_name = 'library/book_detail.html'
    model = Book
    form_class = CommentForm

    def test_func(self):
        is_draft = self.get_object().draft
        is_superuser = self.request.user.is_superuser
        condition = not is_draft or (is_draft and is_superuser)
        return condition

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def form_valid(self, form):
        obj = self.get_object()
        comment = form.save(commit=False)
        comment.content_object = obj
        comment.author = self.request.user
        comment.save()
        return super(BookDetailView, self).form_valid(form)


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'library/book_update.html'
    model = Book
    form_class = BookForm
    permission_required = ['library.change_book']


class BookCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'library/book_create.html'
    model = Book
    form_class = BookForm
    permission_required = ['library.add_book']


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'library/book_delete.html'
    model = Book
    permission_required = ['library.delete_book']

    def get_success_url(self):
        return reverse('library:book_list')


class CommentDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        if self.get_object().author == self.request.user or self.request.user.is_superuser:
            return True
        return False

    def get_success_url(self):
        obj = self.get_object()
        return reverse('library:book_detail', args=(obj.content_object.id,))


class StatisticsView(TemplateView):
    template_name = 'library/statistics.html'

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)

        size_queryset = Book.objects.order_by('size').values_list('size', 'title')
        context['size_labels'] = [book[1] for book in size_queryset]
        context['size_values'] = [book[0] for book in size_queryset]

        page_queryset = Book.objects.order_by('page_count').values_list('page_count', 'title')
        context['page_count_labels'] = [book[1] for book in page_queryset]
        context['page_count_values'] = [book[0] for book in page_queryset]

        return context
