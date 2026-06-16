from django.urls import path, include

from . import views

app_name = "accounts"

urlpatterns = [
    path("api/", include("accounts.api.urls", namespace="accounts_api")),
    path("web/", include("accounts.web.urls", namespace="accounts_web")),
    path("registrasi-akun/", views.RegistrasiAkunView.as_view(), name="registrasi_akun"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]