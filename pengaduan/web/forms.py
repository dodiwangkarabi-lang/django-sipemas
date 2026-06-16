from django import forms

# models
from pengaduan.models import (
    Pengaduan, StatusLaporan, 
    RiwayatStatus
)

class PengaduanForm(forms.ModelForm):
    class Meta:
        model = Pengaduan
        fields = ["judul", "kategori", "isi_laporan", "foto_bukti"]
        
class VerifikasiLaporanForm(forms.ModelForm):
    class Meta:
        model = RiwayatStatus
        fields = ["status", "keterangan"]