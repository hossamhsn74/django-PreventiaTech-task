from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "body")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "post")


