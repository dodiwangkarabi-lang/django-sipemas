# services

# models
from django.contrib.auth.models import User
from accounts.models import (
    Masyarakat
)

class KelolaDataPengguna:
    def __init__(self):
        pass
    
    def delete(self, user_id):
        # hapus masyarakat dan user
        user = User.objects.get(id=user_id)
        user.delete()
        
    def update(self, id, data_masyarakat={}):
        # update masyarakat
        masyarakat = Masyarakat.objects.get(id=id)
        masyarakat.nik = data_masyarakat.get("nik", masyarakat.nik)
        masyarakat.nama = data_masyarakat.get("nama", masyarakat.nama)
        masyarakat.alamat = data_masyarakat.get("alamat", masyarakat.alamat)
        masyarakat.no_hp = data_masyarakat.get("no_hp", masyarakat.no_hp)
        masyarakat.save()
        
        return masyarakat