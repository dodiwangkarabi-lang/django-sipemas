# services

# models
from pengaduan.models import (
    Pengaduan
)
from accounts.models import (
    Masyarakat
)

class LihatRiwayatPengaduan:
    def __init__(self):
        pass
    
    def execute(self, masyarakat):
        qs = Pengaduan.objects.filter(masyarakat=masyarakat)
        return qs