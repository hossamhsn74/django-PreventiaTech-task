from .models import CustomUser, Profile
from .serializers import CustomUserSerializer, RegistrationSerializer, LoginSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from post.serializers import PostSerializer
from post.models import Post


class CustomUserListView(generics.ListAPIView):
    """  
    List All users 
    """
    # permission_classes = [
    #     permissions.IsAuthenticated, permissions.IsAdminUser]
    renderer_classes = (JSONRenderer,)
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class UserSignUpView(generics.CreateAPIView):
    """  
    User Signup View
    """
    permission_classes = [permissions.AllowAny, ]
    renderer_classes = (JSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """  
    User Login View 
    """
    permission_classes = [permissions.AllowAny, ]
    renderer_classes = (JSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    """  
    user pofile view 
    """
    # permission_classes = [permissions.IsAuthenticated, ]
    renderer_classes = (JSONRenderer,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related('user')

    def retrieve(self, request, pk, *args, **kwargs):

        try:
            profile = self.queryset.get(user__pk=pk)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist.')

        serializer = self.serializer_class(profile, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfilePostRetrieveAPIView(generics.RetrieveAPIView):
    """  
    user owned posts view 
    """
    # permission_classes = [permissions.IsAuthenticated, ]
    renderer_classes = (JSONRenderer,)
    serializer_class = PostSerializer
    queryset = Post.objects.select_related('author')

    def retrieve(self, request, pk, *args, **kwargs):

        try:
            posts = self.queryset.get(author__pk=pk)
        except Post.DoesNotExist:
            raise NotFound('A Post with this username does not exist.')

        serializer = self.serializer_class(posts, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)


# class ProfileDeactivateAPIView(generics.DestroyAPIView):
#     # permission_classes = [permissions.IsAdminUser, ]
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

#     def get_object(self):
#         return CustomUser.objects.get(pk=self.kwargs.get('pk'))

#     def destroy(self, request, *args, **kwargs):
#         super(ProfileDeactivateAPIView, self).retrieve(request, args, kwargs)
#         instance = self.get_object()
#         instance.is_active = False
#         serializer = self.get_serializer(instance)
#         data = serializer.data
#         response = {"status_code": status.HTTP_200_OK,
#                     "message": "Successfully deactivated",
#                     "result": data}
#         return Response(response)


class ProfileDeactivateAPIView(generics.DestroyAPIView):
    """
    Deactivate indivdual user.
    """
    # permission_classes = [permissions.IsAuthenticated,]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully delete",
                    "result": data}
        return Response(response)
