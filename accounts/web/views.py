from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
# import Q
from django.db.models import Q

from django_tables2 import RequestConfig

# messages
from django.contrib import messages

# forms
from accounts.web.forms import (
    MasyarakatForm, UserForm
)
from django.contrib.auth.forms import PasswordChangeForm


# tables
from accounts.web.tables import AccountTable

# models
from accounts.models import Masyarakat
from django.contrib.auth.models import User

# repository
from accounts.repositories.akun_repository import AkunRepository

# update_session_auth_hash
from django.contrib.auth import update_session_auth_hash

class RubahPasswordView(View):
    def post(self, request, masyarakat_id, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            
            return redirect(reverse('accounts:accounts_web:detail', args=[masyarakat_id]))
        else:
            messages.error(request, 'Gagal rubah password')
            messages.error(request, form.errors)
            return redirect(reverse('accounts:accounts_web:detail', args=[masyarakat_id]))

class AccountDetailView(View):
    def get(self, request, masyarakat_id, *args, **kwargs):
        rubah_password_form = PasswordChangeForm(request.user)
        
        masyarakat = Masyarakat.objects.get(id=masyarakat_id)
        user = masyarakat.user
        
        masyarakat_form = MasyarakatForm(instance=masyarakat)
        user_form = UserForm(instance=user)
        
        # masyarakat = Masyarakat.objects.get(user_id=user_id)
        
        context = {
            "masyarakat_form": masyarakat_form,
            "user_form": user_form,
            "rubah_password_form": rubah_password_form,
            "user": request.user,
            "masyarakat": masyarakat,
        }
        return render(request, 'accounts/pages/account_detail.html', context)
    
    def post(self, request, masyarakat_id, *args, **kwargs):
        masyarakat = Masyarakat.objects.get(id=masyarakat_id)
        user = masyarakat.user
        
        masyarakat_form = MasyarakatForm(request.POST, instance=masyarakat)
        user_form = UserForm(request.POST, instance=user)
        
        if masyarakat_form.is_valid() and user_form.is_valid():
            masyarakat_form.save()
            user_form.save()
            
            messages.success(request, 'Update akun berhasil')
            return redirect(reverse('accounts:accounts_web:detail', args=[masyarakat_id]))
        else:
            messages.error(request, 'Update akun gagal')
            messages.error(request, masyarakat_form.errors)
            messages.error(request, user_form.errors)
            
            context = {
                "masyarakat_form": masyarakat_form,
                "user_form": user_form,
                "user": request.user,
                "masyarakat": masyarakat
            }
            return render(request, 'accounts/pages/account_detail.html', context)

class AccountView(View):
    def get(self, request, *args, **kwargs):
        repo = AkunRepository()
        masyarakat_qs = repo.akun_masyarakat()
        petugas_qs = repo.akun_petugas()
        
        account_masyarakat_keyword = request.GET.get("account_masyarakat_q", "")
        queryset = masyarakat_qs
        # queryset = Pengaduan.objects.all()
        if account_masyarakat_keyword:
            queryset = queryset.filter(
                Q(nama__icontains=account_masyarakat_keyword)
                
            )
        
        masyarakata_table = AccountTable(queryset)
        petugas_table = AccountTable(petugas_qs)
        
        RequestConfig(
            request, paginate=True
        ).configure(masyarakata_table)
        
        RequestConfig(
            request, paginate=True
        ).configure(petugas_table)
        
        context = {
            "masyarakat_table": masyarakata_table,
            "petugas_table": petugas_table,
            "account_masyarakat_keyword": account_masyarakat_keyword
        }
        return render(request, 'accounts/pages/account.html', context)