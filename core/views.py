from django.shortcuts import render
from django.http import HttpResponse

# login_required
from django.contrib.auth.decorators import login_required

# services
from pengaduan.usecases.lihat_statistik_pengaduan import LihatStatistikPengaduan

@login_required(login_url='accounts:login')
def landing_page(request):
    statistik = LihatStatistikPengaduan().execute()
    
    context = {
        **statistik
    }
    
    return render(request, 'core/pages/landing_page.html', context)
