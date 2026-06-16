from django.contrib.auth.models import User

# models
from accounts.models import Masyarakat, Petugas

class AkunRepository:
    def __init__(self):
        pass
    
    def akun_masyarakat(self):
        # akun dengan group nama masyarakat
        qs = User.objects.filter(groups__name="masyarakat")
        masyarakat_qs = Masyarakat.objects.filter(user__in=qs)
        return masyarakat_qs
    
    def akun_petugas(self):
        # akun dengan group nama petugas
        qs = User.objects.filter(groups__name="petugas")
        petugas_qs = Petugas.objects.filter(user__in=qs)
        return petugas_qs