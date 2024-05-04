from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.db.models import Q

from apps.personal_area.forms import CommentForm
from apps.personal_area.models import Comment
from .models import *
from .forms import *


class PostListView(ListView):
    template_name = 'blog/post_list.html'
    model = Post
    paginate_by = 10

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        if self.request.user.is_superuser:
            return queryset
        if self.request.user.is_anonymous:
            return queryset.exclude(draft=True)        
        return queryset.filter(Q(draft=False) | Q(author=self.request.user))


class CategoryPostListView(PostListView):
    template_name = 'blog/post_list_category.html'
    category = None

    def get_queryset(self):
        queryset = super(CategoryPostListView, self).get_queryset()
        self.category = Category.objects.get(id=self.kwargs['category'])
        queryset = queryset.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryPostListView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostDetailView(DetailView, UserPassesTestMixin, ProcessFormView, FormMixin):
    template_name = 'blog/post_detail.html'
    model = Post
    form_class = CommentForm

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        obj = self.get_object()
        if obj.draft and obj.author == self.request.user:
            return True
        return not obj.draft

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def form_valid(self, form):
        obj = self.get_object()
        comment = form.save(commit=False)
        comment.content_object = obj
        comment.author = self.request.user
        comment.save()
        return super(PostDetailView, self).form_valid(form)


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'blog/post_update.html'
    model = Post
    form_class = PostForm
    permission_required = ['blog.change_post']


class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'blog/post_create.html'
    model = Post
    form_class = PostForm
    permission_required = ['blog.create_post']
    object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'blog/post_delete.html'
    model = Post
    permission_required = ['blog.delete_post']

    def get_success_url(self):
        return reverse('blog:post_list')


class CommentDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        if self.get_object().author == self.request.user or self.request.user.is_superuser:
            return True
        return False

    def get_success_url(self):
        obj = self.get_object()
        return reverse('blog:post_detail', args=(obj.content_object.id,))
