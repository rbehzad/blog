from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from post.models import Post


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter username...'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter password...'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm password...'})



class AddPost(forms.ModelForm):
     class Meta:
         model = Post
         fields = ('title', 'category', 'content', 'tag', 'image')
         labels = {
             'title': '',
             'category': 'Category',
             'content': '',
             'tag': 'Tag',
             'image': '',
         }
         widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title...'}),
             'category': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Enter Category...'}),
             'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Content...'}),
             'tag': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Enter Tag...'}),
         }
