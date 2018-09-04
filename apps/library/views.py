from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django_filters.views import FilterMixin

from apps.personal_area.forms import CommentForm
from .filtersets import BookFilterSet
from .models import *
from .forms import *


class BookListView(FilterMixin, ListView):
    template_name = 'library/book_list.html'
    model = Book
    paginate_by = 24
    filterset_class = BookFilterSet

    def get_queryset(self):
        qs = super(BookListView, self).get_queryset().filter(draft=False)
        return qs

    def get_context_data(self, **kwargs):
        filterset = self.get_filterset(self.get_filterset_class())
        kwargs['filter'] = filterset
        kwargs['object_list'] = filterset.qs
        return super().get_context_data(**kwargs)


class CategoryBookListView(BookListView):
    template_name = 'library/category_book_list.html'
    category = None

    def get_queryset(self):
        queryset = super(CategoryBookListView, self).get_queryset()
        category = self.kwargs.get('category')
        if category != 'none':
            self.category = Category.objects.get(id=category)
        else:
            self.category = None
        queryset = queryset.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryBookListView, self).get_context_data(**kwargs)
        context['category'] = self.category or 'none'
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

    def get_context_data(self, **kwargs):
        context = super(BookUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            book_file_formset = BookFileFormset(self.request.POST,
                                                instance=self.object)
        else:
            book_file_formset = BookFileFormset(instance=self.object)
        context['book_file_formset'] = book_file_formset
        return context

    def form_valid(self, form):
        obj = super(BookUpdateView, self).form_valid(form=form)
        formset = self.get_context_data(**self.kwargs)['book_file_formset']
        if formset.is_valid():  # TODO: Заваливать валидацию полностью, если невалидный формсет
            formset.save()
        return obj


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
