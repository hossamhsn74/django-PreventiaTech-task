from rest_framework import serializers
# from ..users.serializers import ProfileSerializer
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    # liked = serializers.SerializerMethodField(
    #     method_name='get_liked'
    # )
    # likesCount = serializers.SerializerMethodField(
    #     method_name='get_likes_count'
    # )
    # author = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # comments = serializers.ReadOnlyField(source='Comment.content')

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'body', 'attachments']

    # def get_liked(self, instance):
    #     request = self.context.get('request', None)
    #     if request is None:
    #         return False

    #     if not request.user.is_authenticated():
    #         return False
    #     return request.user.profile.has_liked(instance)

    # def get_likes_count(self, instance):
    #     return instance.liked_by.count()


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', ]
