# services
from pengaduan.services.pengaduan import PengaduanService

# models
from pengaduan.models import (
    Pengaduan
)

class LihatStatistikPengaduan:
    def __init__(self):
        self.pengaduan_service = PengaduanService()
        
    def execute(self):
        qs = Pengaduan.objects.all()
        hasil = self.pengaduan_service.statistik(qs)
        return hasil