# login services

# ----- models -----
from django.contrib.auth.models import User, Group
from accounts.models import Petugas, Masyarakat

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

def daftar_akun(*, username, email, password, nik, nama, alamat, no_hp):
    """
    Simpan data (Masyarakat dan User)

    Args:
        username (_type_): _description_
        email (_type_): _description_
        password (_type_): _description_
        nik (_type_): _description_
        nama (_type_): _description_
        alamat (_type_): _description_
        no_hp (_type_): _description_

    Returns:
        user: User
    """
    user = User.objects.create_user(
        username=username,
        email=email,
        # password=make_password(password) # karna sudah otomatis di hash
        password=password
    )
    
    # ----- simpan masyarakat -----
    masyarakat = Masyarakat.objects.create(
        user=user,
        nik=nik,
        nama=nama,
        alamat=alamat,
        no_hp=no_hp
    )
    
    # ----- masukkan dalam nama masyarakat tabel groups -----
    group = Group.objects.get(name="masyarakat")
    group.user_set.add(user)
    
    return user
    

def login_user(request, username, password):
    user = authenticate(
        request=request, username=username, password=password
    )
    if not user:
        return None
    
    login(request, user)
    
    return user

def logout_user(request):
    logout(request)
