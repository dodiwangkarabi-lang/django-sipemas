from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

# import Q
from django.db.models import Q

# messages
from django.contrib import messages

# django-tables2
from django_tables2 import SingleTableView, RequestConfig

# table
from .tables import PengaduanTable

# auth
from django.utils.decorators import method_decorator
# login_reuqired
from django.contrib.auth.decorators import login_required

# forms
from .forms import (
    PengaduanForm, VerifikasiLaporanForm
)

# models
from pengaduan.models import (
    Pengaduan
)

# usecases
from pengaduan.usecases.mengirim_pengaduan import KirimPengaduan
from pengaduan.usecases.verifikasi_laporan import VerifikasiLaporan
from pengaduan.usecases.lihat_riwayat_pengaduan import LihatRiwayatPengaduan
from pengaduan.usecases.lihat_status_laporan import LihatStatusLaporan
from pengaduan.usecases.verifikasi_laporan import VerifikasiLaporan
from pengaduan.usecases.lihat_daftar_pengaduan import LihatDaftarPengaduan

@method_decorator(login_required, name='dispatch')
class PengaduanView(View):
    def get(self, request, *args, **kwargs):
        uc = LihatDaftarPengaduan()
        daftar_pengaduan = uc.semua()
        
        keyword = request.GET.get("q", "")
        queryset = daftar_pengaduan
        # queryset = Pengaduan.objects.all()
        if keyword:
            queryset = queryset.filter(
                Q(judul__icontains=keyword)
                
            )
        
        # table
        table = PengaduanTable(queryset)
        # table = PengaduanTable(daftar_pengaduan)
        RequestConfig(
            request, paginate=True
        ).configure(table)
        
        
        form = PengaduanForm(
            request.POST or None, request.FILES or None
        )
        
        form_verifikasi_laporan = VerifikasiLaporanForm()
        
        if request.method == "POST" and form.is_valid():
            data = form.cleaned_data.copy()
            
            data["masyarakat"] = request.user.masyarakat 
            KirimPengaduan().execute(data)
            
            return redirect(reverse("pengaduan:pengaduan_web:index"))
        
        context = {
            "daftar_pengaduan": daftar_pengaduan,
            "form": form,
            "form_verifikasi_laporan": form_verifikasi_laporan,
            "table": table,
            "keyword": keyword
        }
        return render(request, 'pengaduan/pages/index.html', context)
    
    def post(self, request, *args, **kwargs):
        form_data = PengaduanForm(request.POST, request.FILES)
        if form_data.is_valid():
            data = form_data.cleaned_data.copy()
            data["masyarakat"] = request.user.masyarakat
            
            uc = KirimPengaduan()
            uc.execute(data=data)
            
            return redirect(reverse("pengaduan:pengaduan_web:index"))
        else:
            messages.error(request, form_data.errors)
            return redirect(reverse("pengaduan:pengaduan_web:index"))


@method_decorator(login_required, name='dispatch')
class VerifikasiLaporanView(View):
    def get(self, request, pengaduan_id, *args, **kwargs):
        pengaduan = Pengaduan.objects.get(id=pengaduan_id)
        form = VerifikasiLaporanForm(request.POST or None)
        context = {
            "pengaduan": pengaduan,
            "form": form
        }
        return render(request, 'pengaduan/pages/verifikasi_laporan.html', context)
    
    def post(self, request, pengaduan_id, *args, **kwargs):
        pengaduan = Pengaduan.objects.get(id=pengaduan_id)
        petugas = request.user.petugas
        data = {
            "status": request.POST.get("status"),
            "keterangan": request.POST.get("keterangan")
        }
        VerifikasiLaporan().execute(petugas=petugas, pengaduan=pengaduan, **data)
        return redirect(reverse("pengaduan:pengaduan_web:index"))

@method_decorator(login_required, name='dispatch')
class LihatStatusLaporanView(View):
    def get(self, request, pengaduan_id, *args, **kwargs):
        uc = LihatStatusLaporan()
        pengaduan = uc.execute(pengaduan_id)
        verifikasi_laporan_form = VerifikasiLaporanForm(request.POST or None)
        context = {
            "pengaduan": pengaduan,
            "verifikasi_laporan_form": verifikasi_laporan_form
        }
        return render(request, 'pengaduan/pages/lihat_status_laporan.html', context)


@method_decorator(login_required, name='dispatch')
class RiwayatPengaduanView(View):
    def get(self, request, *args, **kwargs):
        form = PengaduanForm()
        uc = LihatRiwayatPengaduan()
        queryset = uc.execute(request.user.masyarakat)
        
        keyword = request.GET.get("q", "")
        # queryset = daftar_pengaduan
        # queryset = Pengaduan.objects.all()
        if keyword:
            queryset = queryset.filter(
                Q(judul__icontains=keyword)
                
            )
        
        # table
        table = PengaduanTable(queryset)
        RequestConfig(
            request, paginate=True
        ).configure(table)
        
        
        context = {
            "riwayat_pengaduan": table,
            "form": form,
            "keyword": keyword
        }
        return render(request, 'pengaduan/pages/riwayat_pengaduan.html', context)

    

# def index(request):
#     form = PengaduanForm(
#         request.POST or None, request.FILES or None
#     )
#     form_verifikasi_laporan = VerifikasiLaporanForm()
    
#     if request.method == "POST" and form.is_valid():
#         data = form.cleaned_data.copy()
        
#         data["masyarakat"] = request.user.masyarakat 
#         KirimPengaduan().execute(data)
        
#         return redirect(reverse("pengaduan:pengaduan_web:index"))
        
#     context = {
#         "form": form,
#         "form_verifikasi_laporan": form_verifikasi_laporan
#     }
#     template_name = 'pengaduan/pages/index.html'
#     return render(request, template_name, context)