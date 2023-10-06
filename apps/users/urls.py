from django.urls import path
from .views import UserRegisterView, UpdateProfileView, ChangePasswordView


urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("update/", UpdateProfileView.as_view(), name="user-update"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
    