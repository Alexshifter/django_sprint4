from datetime import datetime

from django.db.models import Count
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import (
    render, get_object_or_404, redirect,
)
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    CreateView, ListView, UpdateView, DeleteView, DetailView,
)

from .models import User, Post, Category, Comment
from .forms import PostForm, ProfileForm, CommentForm


POST_PER_PAGES = 10


def get_res_qs(my_object):
    return my_object.filter(
        is_published=True,
        pub_date__lt=datetime.now(),
        category__is_published=True,).select_related(
            'category',
            'author',
            'location',
    ).order_by('-pub_date').annotate(comment_count=Count('comments'),)


@login_required
def edit_profile(request, username):
    instance = get_object_or_404(User, username=username)
    template = 'blog/user.html'
    form = ProfileForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=username)
    return render(request, template, context)


class PostFormMixin:
    form_class = PostForm
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'


class CommentFormMixin:
    form_class = CommentForm
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'id': self.kwargs['post_id']},
        )


class UserView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = POST_PER_PAGES
    pk = 'username'

    def get_queryset(self):
        return Post.objects.filter(
            author__username=self.kwargs[self.pk]).annotate(
            comment_count=Count('comments')).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(
            User,
            username=self.kwargs.get(self.pk),
        )
        context['profile'] = author
        return context


class PostCreateView(PostFormMixin, LoginRequiredMixin, CreateView):
    pk_url_kwarg = None

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(PostFormMixin, LoginRequiredMixin, UpdateView):

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Post,
            id=kwargs['post_id'],
        )
        if instance.author != request.user:
            return redirect(
                reverse(
                    'blog:post_detail',
                    kwargs={'id': self.kwargs[self.pk_url_kwarg]},
                )
            )
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(PostFormMixin, LoginRequiredMixin, DeleteView):

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Post,
            id=kwargs[self.pk_url_kwarg],
        )
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(
            self.request.POST or None,
            instance=self.object,
        )
        return context

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user},
        )


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = POST_PER_PAGES

    def get_queryset(self):
        return get_res_qs(Post.objects)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Post,
            id=self.kwargs['id']
        )
        if ~(instance.is_published) & (instance.author != request.user):
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = POST_PER_PAGES
    slug_url_kwarg = 'category_slug'

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs.get('category_slug'),
            is_published='True',
        )
        return get_res_qs(category.posts_in_category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_category = get_object_or_404(
            Category,
            slug=self.kwargs.get(self.slug_url_kwarg),
            is_published='True',
        )
        context['category'] = selected_category
        return context


class CommentAddView(LoginRequiredMixin, CommentFormMixin, CreateView):
    pk_url_kwarg = 'post_id'
    selected_post = None
    template_name = None

    def dispatch(self, request, *args, **kwargs):
        self.selected_post = get_object_or_404(
            Post,
            id=kwargs[self.pk_url_kwarg],
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.selected_post
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, CommentFormMixin, UpdateView):

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Comment,
            id=kwargs[self.pk_url_kwarg]
        )
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, CommentFormMixin, DeleteView):

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Comment, id=kwargs[self.pk_url_kwarg]
        )
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
