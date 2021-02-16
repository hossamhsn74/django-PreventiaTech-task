from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView, CommentDetailView, CommentListView
app_label = 'post'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='postlist'),
    path('posts/create/', PostCreateView.as_view(), name='createpost'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='detailviewpost'),
    path('posts/<int:pk>/comments',
         CommentListView.as_view(), name='postCommentslist'),
    path('posts/<int:post_id>/comments/<int:pk>',
         CommentDetailView.as_view(), name='postComment'),
    # path('posts/<int:pk>/comments/add', CommentCreateView.as_view(), name='addComment'),
    # path('posts/<int:pk>/like', CommentCreateView.as_view(), name='addComment'),
]
