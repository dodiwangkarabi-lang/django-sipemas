# services

# models
from pengaduan.models import (
    Pengaduan
)

class LihatStatusLaporan:
    def __init__(self):
        pass
    
    def execute(self, pengaduan_id):
        return Pengaduan.objects.get(id=pengaduan_id)