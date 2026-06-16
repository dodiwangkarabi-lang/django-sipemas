from django.contrib import admin

# models
from pengaduan.models import (
    Pengaduan, RiwayatStatus
)

admin.site.register(Pengaduan)
admin.site.register(RiwayatStatus)