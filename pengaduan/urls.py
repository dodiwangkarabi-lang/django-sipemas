from django.urls import path, include

app_name = "pengaduan"

urlpatterns = [
    path("", include("pengaduan.web.urls")),
]