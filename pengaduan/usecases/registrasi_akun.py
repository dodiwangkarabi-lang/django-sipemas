# usecase registrasi akun

from django.contrib.auth.models import User, Group
from django.db import transaction

# model
from accounts.models import (
    Masyarakat
)

class RegistrasiAkun:
    def __init__(self):
        pass
    
    def execute(self, **kwargs):
        """
        pendaftar akun oleh masyarakat
        
        Kwargs:
            username (str): _description_
            password (str): _description_
            email (str): _description_
            nik (str): _description_
            nama (str): _description_
            alamat (str): _description_
            no_hp (str): _description_

        Returns:
            _type_: _description_
            
        """
        data_user = {
            "username": kwargs["username"],
            "password": kwargs["password"],
            "email": kwargs["email"]
        }
        
        data_masyarakat = {
            "nik": kwargs["nik"],
            "nama": kwargs["nama"],
            "alamat": kwargs["alamat"],
            "no_hp": kwargs["no_hp"]
        }
        
        with transaction.atomic():
            # buat user
            user = User.objects.create_user(**data_user)
            
            # buat group masyarakat
            group = Group.objects.get(name="masyarakat")
            group.user_set.add(user)
            
            # buat masyarakat
            masyarakat = Masyarakat.objects.create(user=user, **data_masyarakat)
            
        return True