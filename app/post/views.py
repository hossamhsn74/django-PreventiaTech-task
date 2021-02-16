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
    permission_classes = [permissions.AllowAny, ]
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', ]


class PostCreateView(generics.CreateAPIView):
    """
    View to add Post to the system.
    * Requires token authentication.
    * Requires Admin User.
    """
    # permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
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
    * Requires token authentication.
    * Requires Admin User.
    """
    # permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
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


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    DetailView for indivdual post.
    * Requires token authentication.
    * Requires Admin User.
    """
    # permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        comment_id = self.kwargs.get('pk')
        return Comment.objects.get(post=post_id, id=comment_id)

    def get(self, request, *args, **kwargs):
        super(CommentDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)


class CommentListView(views.APIView):
    """
    List All Comments for specific Post
    * Requires token authentication.
    * Requires Admin User.
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


# class CommentCreateView(generics.CreateAPIView):
#     """
#     View to add a new Comment.

#     * Requires token authentication.
#     * Only admin users are able to access this view.
#     """
#     # authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
#     queryset = Comment.objects.all()
#     serializer_class = serializers.CommentSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     super(CommentCreateView, self).create(request, args, kwargs)
    #     response = {"status_code": status.HTTP_200_OK,
    #                 "message": "Successfully added to books",
    #                 "result": request.data}
    #     return Response(response)
