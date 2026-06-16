
from django.urls import path

from . import views

app_name = "accounts_web"

urlpatterns = [
    path("<int:masyarakat_id>/", views.AccountDetailView.as_view(), name="detail"),
    path("rubah-password/<int:masyarakat_id>/", views.RubahPasswordView.as_view(), name="rubah_password"),
    path("", views.AccountView.as_view(), name="index"),
]