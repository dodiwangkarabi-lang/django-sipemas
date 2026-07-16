from django.urls import path

from . import views

app_name = "pengaduan_api"

urlpatterns = [
    path("<int:pengaduan_id>/daftar-status/", views.PengaduanDaftarStatusView.as_view(), name="pengaduan_daftar_status"),
    path("<int:pengaduan_id>/update-status/", views.PengaduanUpdateStatusView.as_view(), name="pengaduan_update_status"),
    path("rangkuman/", views.PengaduanRangkumanView.as_view(), name="pengaduan_rangkuman"),
    path("create/", views.PengaduanCreateView.as_view(), name="pengaduan_create"),
    path("list/", views.PengaduanListView.as_view(), name="pengaduan_list"),
    path("<int:pengaduan_id>/", views.PengaduanDetailView.as_view(), name="pengaduan_detail"),
    path("", views.PengaduanView.as_view(), name="index"),
]