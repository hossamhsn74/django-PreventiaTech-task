from .models import Post, Comment
from . import serializers
from rest_framework import generics, status, filters, views
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from django.shortcuts import get_object_or_404
from django.http import Http404


class PostListView(generics.ListAPIView):
    """
    View to list all Posts in the system.
    """
    # permission_classes = [permissions.IsAuthenticated, ]
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', ]


class PostCreateView(generics.CreateAPIView):
    """
    View to add Post to the system.
    """
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def create(self, request, *args, **kwargs):
        super(PostCreateView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully added new Post",
                    "result": request.data}
        return Response(response)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    DetailView for indivdual post.
    """
    # permission_classes = [permissions.IsAuthenticated,]
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def retrieve(self, request, *args, **kwargs):
        super(PostDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(PostDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully updated",
                    "result": data}
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(PostDetailView, self).delete(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully deleted"}
        return Response(response)


class CommentListView(generics.ListAPIView):
    """
    View to list all Comments in the system.
    """
    permission_classes = [permissions.AllowAny, ]
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', ]


class CommentCreateView(generics.CreateAPIView):
    """
    View to add Comment to the system.
    """
    # permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def create(self, request, *args, **kwargs):
        super(CommentCreateView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully added new Comment",
                    "result": request.data}
        return Response(response)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    DetailView for indivdual comment in general.
    """
    # permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def retrieve(self, request, *args, **kwargs):
        super(CommentDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(CommentDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully updated",
                    "result": data}
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(CommentDetailView, self).delete(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully deleted"}
        return Response(response)


class PostCommentListView(views.APIView):
    """
    Get all comments for specific Post
    """
    # permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        comments = self.get_object(pk)
        serializer = serializers.CommentSerializer(comments)
        return Response(serializer.data)


class PostCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get specific comment on specific post
    """
    # permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        comment_id = self.kwargs.get('pk')
        return Comment.objects.get(post=post_id, id=comment_id)

    def get(self, request, *args, **kwargs):
        super(PostCommentDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)
