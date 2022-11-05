from django.contrib import admin
from post.models import Post, Comment, Category, Profile, Like


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'posted')
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Like)
