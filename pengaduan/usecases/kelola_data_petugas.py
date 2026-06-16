# services

# models
from django.contrib.auth.models import User
from accounts.models import (
    Petugas
)

class KelolaDataPengguna:
    def __init__(self):
        pass
    
    def delete(self, user_id):
        # hapus petugas dan user
        user = User.objects.get(id=user_id)
        user.delete()
        
    def update(self, id, data_petugas={}):
        # update petugas
        petugas = petugas.objects.get(id=id)
        petugas.nik = data_petugas.get("nik", petugas.nik)
        petugas.nama = data_petugas.get("nama", petugas.nama)
        petugas.alamat = data_petugas.get("alamat", petugas.alamat)
        petugas.no_hp = data_petugas.get("no_hp", petugas.no_hp)
        petugas.save()
        
        return petugas
        