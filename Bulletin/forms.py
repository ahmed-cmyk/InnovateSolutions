from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    title = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Title', 'class': 'form-control'}
    ))

    feed = forms.CharField(required=True, max_length=5000, widget=forms.Textarea(
        attrs={'placeholder': 'Enter information for bulletin board', 'class': 'form-control'}
    ))

    class Meta:
        model = Post
        fields = ('title', 'feed', 'status')
        exclude = ('release_date', 'update_date', 'author')
