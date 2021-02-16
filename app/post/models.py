from django.db import models
from core.models import TimestampedModel


class Post(TimestampedModel):
    # author = models.ForeignKey(
    #     'users.Profile', on_delete=models.CASCADE, related_name='user_posts'
    # )
    title = models.CharField(db_index=True, max_length=255)
    body = models.TextField()
    attachments = models.FileField(upload_to='files/', blank=True)

    def __str__(self):
        return self.title


class Comment(TimestampedModel):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    # author = models.ForeignKey(
    #     'users.Profile', on_delete=models.CASCADE, related_name='user_comments'
    # )
    content = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.content
