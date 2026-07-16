# ----- dto -----
from pengaduan.dtos import TimeLineDTO

# ----- models -----
from pengaduan.models import RiwayatStatus, Pengaduan, StatusLaporan

class TimeLineService:
    
    @staticmethod
    def update(timeline: TimeLineDTO) -> RiwayatStatus:
        obj = RiwayatStatus.objects.get(
            pengaduan_id=timeline.pengaduan_id
        )
        obj.petugas_id = timeline.petugas_id
        obj.status = timeline.status
        obj.keterangan = timeline.keterangan
        obj.save()
        
        return obj
    
    @staticmethod
    def create(timeline: TimeLineDTO) -> RiwayatStatus:
        obj = RiwayatStatus.objects.create(
            pengaduan_id=timeline.pengaduan_id,
            petugas_id=timeline.petugas_id,
            status=timeline.status,
            keterangan=timeline.keterangan
        )
        
        # ----- update status pengaduan -----
        pengaduan = Pengaduan.objects.get(id=timeline.pengaduan_id)
        pengaduan.status = timeline.status
        pengaduan.save()
        
        return obj
    
    @staticmethod
    def update_or_create(timeline: TimeLineDTO) -> tuple[bool, RiwayatStatus]:
        created = False
        try:
            return created, TimeLineService.update(timeline)
        except RiwayatStatus.DoesNotExist:
            created = True
            return created, TimeLineService.create(timeline)
        