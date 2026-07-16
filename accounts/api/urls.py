
from django.urls import path

from . import views

app_name = "accounts_api"

urlpatterns = [
    path("daftar/", views.DaftarMasyarakatAPIView.as_view(), name="daftar"),
    path("ubah-password/", views.UbahPasswordAPIView.as_view(), name="ubah_password"),
    path("update-profile-masyarakat/", views.UpdateProfileMasyarakatAPIView.as_view(), name="update_profile_masyarakat"),
    path("me/", views.AccountView.as_view(), name="me"),
]