from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse

# messages
from django.contrib import messages

# usecases
from pengaduan.usecases.login import Login, Logout
from pengaduan.usecases.registrasi_akun import RegistrasiAkun

# form
from .forms import UserForm, MasyarakatForm

class RegistrasiAkunView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/pages/registrasi_akun.html')
    
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST or None)
        masyarakat_form = MasyarakatForm(request.POST or None)

        if user_form.is_valid() and masyarakat_form.is_valid():
            user_data = user_form.cleaned_data
            masyarakat_data = masyarakat_form.cleaned_data

            data = {
                "username": user_data['username'],
                "password": user_data['password1'],
                "email": user_data['email'],
                "nik": masyarakat_data['nik'],
                "nama": masyarakat_data['nama'],
                "alamat": masyarakat_data['alamat'],
                "no_hp": masyarakat_data['no_hp'],
            }
        
            uc = RegistrasiAkun().execute(**data)
        else:
            messages.error(request, 'Registrasi akun gagal')
            # pesan error dari form
            messages.error(request, user_form.errors)
            messages.error(request, masyarakat_form.errors)
            
            # return redirect(reverse('accounts:registrasi_akun'))
            return render(request, 'accounts/pages/registrasi_akun.html')
            
            
        return redirect(reverse('accounts:login'))


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        uc = Logout().execute(request)
        return redirect(reverse('accounts:login'))

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/pages/login.html')
    
    def post(self, request, *args, **kwargs):
        uc = Login()
        res = uc.execute(
            request=request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        
        if res:
            return redirect(reverse('core:landing_page'))
        else:
            messages.error(request, 'Username atau password salah')
            return render(request, 'accounts/pages/login.html')
