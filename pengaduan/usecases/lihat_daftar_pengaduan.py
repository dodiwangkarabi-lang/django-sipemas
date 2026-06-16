# services

# models
from pengaduan.models import (
    Pengaduan,
    StatusLaporan
)

class LihatDaftarPengaduan:
    def __init__(self):
        pass
    
    def semua(self):
        return Pengaduan.objects.all()
    
    def status_menunggu(self):
        return Pengaduan.objects.filter(status=StatusLaporan.MENUNGGU)
    