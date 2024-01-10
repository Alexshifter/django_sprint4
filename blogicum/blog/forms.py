from django import forms

from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(
                attrs={'type': 'date'},
                format=('%Y-%m-%d')
            )
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
