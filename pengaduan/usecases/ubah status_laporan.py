# services

# models
from pengaduan.models import (
    Pengaduan,
    StatusLaporan
)

class UbahStatusLaporan:
    def __init__(self):
        pass
    
    def execute(self, pengaduan, status):
        pengaduan.status = status
        pengaduan.save()
        return True