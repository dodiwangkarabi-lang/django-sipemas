# services
from pengaduan.services.pengaduan import PengaduanService

# ----- selectors -----
from pengaduan.selectors import get_pengaduan_by_role

# models
from pengaduan.models import (
    Pengaduan
)

class LihatStatistikPengaduan:
    def __init__(self):
        self.pengaduan_service = PengaduanService()
        
    def execute(self, user):
        qs = get_pengaduan_by_role(user)
        hasil = self.pengaduan_service.statistik(qs)
        return hasil