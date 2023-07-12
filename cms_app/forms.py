from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Comment, Reply


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class CreatePostForm(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = Post
        exclude = ['slug', 'author']

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'author']

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Join the discussion and leave a comment!'}))
    class Meta:
        model = Comment
        fields = ['content']


class ReplyForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Leave a reply!'}))
    class Meta:
        model = Reply
        fields = ['content']
        labels = {
            "content": ""
        }



        