# usecase verifikasi laporan

# model
from pengaduan.models import (
    Pengaduan, RiwayatStatus
)
from accounts.models import (
    Petugas
)

class VerifikasiLaporan:
    def __init__(self):
        pass
    
    def execute(self, pengaduan: Pengaduan, petugas: Petugas, **kwargs):
        """
        melakukan verifikasi

        Args:
            pengaduan (Pengaduan): _description_
            petugas (Petugas): _description_
            
        Kwargs:
            status (str): 
                status laporan misalnya "diproses", "selesai", "menunggu"
            keterangan (str): 
                catatan yang dibuat oleh petugas
        """
        data = {
            "status": kwargs.get("status"),
            "keterangan": kwargs.get("keterangan")
        }
        
        # verifikasi laporan pengaduan
        # obj, created = RiwayatStatus.objects.update_or_create(
        #     pengaduan=pengaduan,
        #     petugas=petugas,
        #     defaults=data
        # )
        
        RiwayatStatus.objects.create(
            pengaduan=pengaduan,
            petugas=petugas,
            **data
        )
        
        # update status laporan
        pengaduan.status = kwargs.get("status")
        pengaduan.save()
        