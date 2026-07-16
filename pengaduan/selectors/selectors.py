# ----- model -----
from pengaduan.models import Pengaduan, RiwayatStatus

from django.db.models import QuerySet

def get_riwayat_status(pengaduan: Pengaduan) -> QuerySet[RiwayatStatus]:
    qs = pengaduan.riwayat_status.all()
    qs = qs.order_by("-tanggal_update")
    return qs

def get_pengaduan_by_role(user) -> QuerySet:
    qs = Pengaduan.objects.select_related(
        "masyarakat"
    )
    
    groups = set(user.groups.values_list("name", flat=True))

    if "masyarakat" in groups:
        return qs.filter(masyarakat=user.masyarakat)

    if "petugas" in groups:
        return qs

    return qs.none()

# def get_pengaduan_by_role(user) -> QuerySet:

#     if user.groups.filter(name="masyarakat").exists():
#         return Pengaduan.objects.filter(masyarakat=user.masyarakat)
    
#     return Pengaduan.objects.none()