from django.db import models
from core.models import TimestampedModel


class Post(TimestampedModel):
    author = models.ForeignKey(
        'users.Profile', related_name='user_posts', on_delete=models.CASCADE, default=1
    )
    title = models.CharField(db_index=True, max_length=255)
    body = models.TextField()
    attachments = models.FileField(upload_to='files/', default=None)

    def __str__(self):
        return self.title


class Comment(TimestampedModel):
    author = models.ForeignKey(
        'users.Profile', related_name='user_comments', on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.content
