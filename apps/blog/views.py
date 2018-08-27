from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from apps.personal_area.forms import CommentForm
from .models import *
from .forms import *


class PostListView(ListView):
    template_name = 'blog/post_list.html'
    model = Post
    paginate_by = 5

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(draft=False)
        return queryset


class CategoryPostListView(PostListView):
    template_name = 'blog/category_post_list.html'
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
