# services

# models
from pengaduan.models import (
    Pengaduan
)

class KirimPengaduan:
    def __init__(self):
        pass
    
    def execute(self, data):
        Pengaduan.objects.create(**data)
        return True