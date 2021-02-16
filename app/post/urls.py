from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView, CommentDetailView, CommentListView, PostCommentListView, PostCommentDetailView, CommentCreateView
app_label = 'post'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='postlist'),
    path('posts/create/', PostCreateView.as_view(), name='createpost'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='detailviewpost'),
    path('comments/', CommentListView.as_view(), name='commentlist'),
    path('comments/create/', CommentCreateView.as_view(), name='createpost'),
    path('comments/<int:pk>', CommentDetailView.as_view(), name='commentlist'),
    path('posts/<int:pk>/comments',
         PostCommentListView.as_view(), name='postCommentslist'),
    path('posts/<int:post_id>/comments/<int:pk>',
         PostCommentDetailView.as_view(), name='postComment'),
    # path('posts/<int:pk>/comments/add', CommentCreateView.as_view(), name='addComment'),
    # path('posts/<int:pk>/like', CommentCreateView.as_view(), name='addComment'),
    # path('posts/<int:pk>/likecount', CommentCreateView.as_view(), name='addComment'),
]
