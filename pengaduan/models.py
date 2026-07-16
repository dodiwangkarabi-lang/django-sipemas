from django.db import models
from django.contrib.auth.models import User

from accounts.models import (
    Masyarakat, Petugas
)
# class StatusLaporan(models.Model):
#     nama_status = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.pk} {self.nama_status}"

# class KategoriPengaduan(models.Model):
#     nama_kategori = models.CharField(max_length=100)
#     deskripsi = models.TextField(blank=True)

#     def __str__(self):
#         return self.nama_kategori
    
class StatusLaporan(models.TextChoices):
    MENUNGGU = "MENUNGGU", "Menunggu"
    DIVERIFIKASI = "DIVERIFIKASI", "Diverifikasi"
    DIPROSES = "DIPROSES", "Diproses"
    SELESAI = "SELESAI", "Selesai"
    DITOLAK = "DITOLAK", "Ditolak"

class KategoriPengaduan(models.TextChoices):
    LAINNYA = "LAINNYA", "Lainnya"
    ASPIRASI = "ASPIRASI", "Aspirasi"
    PERMASALAHAN = "PERMASALAHAN", "Permasalahan"
    PERINGATAN = "PERINGATAN", "Peringatan"
    PERTANYAAN = "PERTANYAAN", "Pertanyaan"



class Pengaduan(models.Model):
    masyarakat = models.ForeignKey(
        Masyarakat,
        on_delete=models.CASCADE,
        related_name='pengaduan'
    )

    kategori = models.CharField(
        max_length=20,
        choices=KategoriPengaduan.choices,
        default=KategoriPengaduan.LAINNYA
    )

    status = models.CharField(
        max_length=20,
        choices=StatusLaporan.choices,
        default=StatusLaporan.MENUNGGU
    )

    judul = models.CharField(max_length=200)
    isi_laporan = models.TextField()

    foto_bukti = models.ImageField(
        upload_to='pengaduan/',
        null=True,
        blank=True
    )

    hasil_klasifikasi = models.CharField(
        max_length=100,
        blank=True
    )

    tanggal_pengaduan = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.pk} - {self.judul}"
    
    class Meta:
        ordering = ['-tanggal_pengaduan']


class RiwayatStatus(models.Model):
    pengaduan = models.ForeignKey(
        Pengaduan,
        on_delete=models.CASCADE,
        related_name='riwayat_status'
    )

    petugas = models.ForeignKey(
        Petugas,
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=StatusLaporan.choices
    )

    keterangan = models.TextField(blank=True)

    tanggal_update = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.pengaduan} - {self.status}"


class Tanggapan(models.Model):
    pengaduan = models.ForeignKey(
        Pengaduan,
        on_delete=models.CASCADE,
        related_name='tanggapan'
    )

    petugas = models.ForeignKey(
        Petugas,
        on_delete=models.SET_NULL,
        null=True
    )

    isi_tanggapan = models.TextField()

    tanggal_tanggapan = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Tanggapan {self.pengaduan}"