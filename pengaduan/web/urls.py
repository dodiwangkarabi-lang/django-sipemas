from django.urls import path
from . import views

app_name = "pengaduan_web"

urlpatterns = [
    path("verifikasi-laporan/<int:pengaduan_id>/", views.VerifikasiLaporanView.as_view(), name="verifikasi_laporan"),
    path("riwayat-pengaduan", views.RiwayatPengaduanView.as_view(), name="riwayat_pengaduan"),
    path("lihat-status-laporan/<int:pengaduan_id>/", views.LihatStatusLaporanView.as_view(), name="lihat_status_laporan"),
    path("verifikasi-laporan/", views.VerifikasiLaporanView.as_view(), name="verifikasi_laporan"),
    path("", views.PengaduanView.as_view(), name="index"),
    # path("", views.index, name="index"),
]