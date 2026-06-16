# models
from pengaduan.models import (
    Pengaduan, StatusLaporan
)


class PengaduanService:
    def __init__(self):
        pass
    
    def statistik(self, daftar_pengaduan):
        """
        statistik pengaduan

        Args:
            daftar_pengaduan (queryset): Queryset dari model Pengajuan

        Returns:
            dict: total_pengaduan, menunggu_verifikasi, sedang_diproses, selesai
        """
        pengaduan = daftar_pengaduan
        total_pengaduan = pengaduan.count()
        menunggu_verifikasi = pengaduan.filter(status=StatusLaporan.MENUNGGU).count()
        sedang_diproses = pengaduan.filter(status=StatusLaporan.DIPROSES).count()
        selesai = pengaduan.filter(status=StatusLaporan.SELESAI).count()
        
        data = {
            "total_pengaduan": total_pengaduan or 0,
            "total_menunggu": menunggu_verifikasi or 0,
            "total_diproses": sedang_diproses or 0,
            "total_selesai": selesai or 0
        }
        return data