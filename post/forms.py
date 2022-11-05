from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from post.models import Comment, Post, Profile


class CommentForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), required=True)

    class Meta:
        model = Comment
        fields = ("body",)


class CreatePostForm(ModelForm):
    title = forms.CharField(required=False)
    body = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    # video = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = 'title', 'category', 'body', 'image'


class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input-text with-border', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input-text with-border', 'placeholder': 'Repeat Password'}))

    class Meta:
        model = User
        fields = 'username', 'email', 'first_name', 'last_name'


class ProfileForm(forms.Form):
    profile_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ('bio', 'profile_image',)


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                                 required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                                required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UpdateProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']
