from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'like_users')

    
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"cols": "40", "rows": "1"},
        )
    )
    class Meta:
        model = Comment
        fields = ('content', )