from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from embed_video.fields import EmbedVideoField


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile_images/',
                                      default='profile_images/default.png')
    username = models.CharField(max_length=100),
    email = models.EmailField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True),

    def __str__(self):
        return str(self.user.username)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=2000, null=True, blank=True, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_created=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    like_count = models.BigIntegerField(default='0')
    image = models.ImageField(upload_to='static/images/%Y/%m', null=True, blank=True)
    video = EmbedVideoField(null=True, blank=True)
    url = EmbedVideoField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post_views = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.likes.all().count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(self.posted))
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-posted']


LIKE_CHOICES = (
    ('lIKE', 'lIKE'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
