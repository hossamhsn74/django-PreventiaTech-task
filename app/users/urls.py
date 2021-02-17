from django.urls import path, include
from .views import CustomUserListView, UserSignUpView, UserLoginView, ProfileRetrieveAPIView, ProfilePostRetrieveAPIView, ProfileDeactivateAPIView

urlpatterns = [
    path("users/", CustomUserListView.as_view()),
    path("users/signup", UserSignUpView.as_view()),
    path("users/login", UserLoginView.as_view()),
    path("users/<int:pk>/profile", ProfileRetrieveAPIView.as_view()),
    path("users/<int:pk>/posts", ProfilePostRetrieveAPIView.as_view()),
    path("users/<int:pk>/deactivate", ProfileDeactivateAPIView.as_view()),
]
