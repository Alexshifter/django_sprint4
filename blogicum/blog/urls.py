from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('profile/<str:username>/', views.UserView.as_view(),
         name='profile'),
    path('edit_profile/<username>/', views.UserUpdateView.as_view(),
         name='edit_profile'),
    path('posts/create/', views.PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:id>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/<int:post_id>/edit/', views.PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/', views.PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<post_id>/comment/', views.CommentAddView.as_view(),
         name='add_comment'),
    path('posts/<post_id>/edit_comment/<comment_id>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'),
    path('posts/<post_id>/delete_comment/<comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),
    path('category/<slug:category_slug>/', views.CategoryListView.as_view(),
         name='category_posts'),
    path('', views.PostListView.as_view(), name='index')
]
