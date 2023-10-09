from django.urls import path
from .views import UserRegisterView, UpdateProfileView, ChangePasswordView, UpdatePhoneView, RecoverPasswordView
from .views import check_phone_number

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("update/", UpdateProfileView.as_view(), name="user-update"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("update-phone/", UpdatePhoneView.as_view(), name="update-phone"),
    path("check-phone/<str:phone_number>/", check_phone_number, name="check-phone"),
    path("recover-password/", RecoverPasswordView.as_view(), name="recover-password")
]
    