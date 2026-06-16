from django.db import transaction

# models
from pengaduan.models import (
    Pengaduan, RiwayatStatus, StatusLaporan
)

# services

# models
from pengaduan.models import (
    Pengaduan
)

class KirimPengaduan:
    def __init__(self):
        pass
    
    def execute(self, data):
        
        with transaction.atomic():
            pengaduan = Pengaduan.objects.create(**data)
            
            # create riwayat status laporan
            RiwayatStatus.objects.create(
                pengaduan=pengaduan,
                status=StatusLaporan.MENUNGGU
            )
            
            # update status laporan
            pengaduan.status = StatusLaporan.MENUNGGU
            pengaduan.save()
        
            return True
        
        return False