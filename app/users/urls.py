from django.urls import path, include
from .views import UserSignUpView, UserLoginView, UserRetrieveUpdateAPIView


urlpatterns = [
    path("user/", UserRetrieveUpdateAPIView.as_view()),
    path("users/", UserSignUpView.as_view()),
    path("users/login", UserLoginView.as_view()),
]
