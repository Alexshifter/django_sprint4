from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import Post, Comment
from .forms import PostForm, CommentForm


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
            kwargs={'id': self.kwargs.get('post_id')},
        )


class CommentFormEditMixin(CommentFormMixin):

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Comment, id=self.kwargs.get(self.pk_url_kwarg)
        )
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
