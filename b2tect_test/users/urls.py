from django.urls import path, include
from .views import RegisterAPIView, AuthAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("auth/", AuthAPIView.as_view()),
]