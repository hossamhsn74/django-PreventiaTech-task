from .models import CustomUser, Profile
from .serializers import CustomUserSerializer, RegistrationSerializer, LoginSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound


class CustomUserListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny, ]
    # renderer_classes = (JSONRenderer,)
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class UserSignUpView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny, ]
    # renderer_classes = (JSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny, ]
    # renderer_classes = (JSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny, ]
    # renderer_classes = (JSONRenderer,)
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


class ProfilePostsRetrieveAPIView(generics.RetrieveAPIView):
    pass
    # permission_classes = [permissions.AllowAny, ]
    # # renderer_classes = (JSONRenderer,)
    # serializer_class = ProfileSerializer
    # queryset = Profile.objects.select_related('user')

    # def retrieve(self, request, pk, *args, **kwargs):

    #     try:
    #         profile = self.queryset.get(user__pk=pk)
    #     except Profile.DoesNotExist:
    #         raise NotFound('A profile with this username does not exist.')

    #     serializer = self.serializer_class(profile, context={
    #         'request': request
    #     })

    #     return Response(serializer.data, status=status.HTTP_200_OK)



class CustomUserChangeView(APIView):
    # allow admin user to deactivate user account
    pass