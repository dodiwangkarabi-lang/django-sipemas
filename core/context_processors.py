# apps/core/context_processors.py
from core.utils.permissions import has_group
from core.constants import *

# services
from accounts.services.permission_service import PermissionService
permission_service = PermissionService()

def sidebar_menu(request):

    menus = []

    if request.user.is_authenticated:
        
        # menu utama
        menus += [
            {
                "title": "Dashboard",
                "url": "core:landing_page",
                "icon": "grid-outline",
                "is_active": request.resolver_match.view_name == "core:landing_page",
            },
            {
                "title": "Pengaduan",
                "url": "pengaduan:pengaduan_web:index",
                "icon": "grid-outline",
                "is_active": request.resolver_match.view_name == "pengaduan:pengaduan_web:index",
            },
            
            # {
            #     "title": "Riwayat Pengaduan",
            #     "url": "pengaduan:pengaduan_web:riwayat_pengaduan",
            #     "icon": "grid-outline",
            #     "is_active": request.resolver_match.view_name == "pengaduan:pengaduan_web:riwayat_pengaduan",
            # },
            
            # {
            #     "title": "Pengaduan",
            #     "url": "academics:siswa:siswa_web:index",
            #     "icon": "people-outline",
            #     "is_active": request.resolver_match.view_name == "academics:siswa:siswa_web:index",
            # },
            
        ]
        
        # petugas
        if permission_service.is_petugas(request.user):
            menus += [
                {
                    "title": "Accounts",
                    "url": "accounts:accounts_web:index",
                    "icon": "grid-outline",
                    "is_active": request.resolver_match.view_name == "accounts:accounts_web:index",
                },
            ]
        
        # admin
        # if has_group(request.user, ROLE_ADMIN):
        #     menus += [
        #         {
        #             "title": "Model",
        #             "url": "predictions:predictions_web:index",
        #             "icon": "analytics-outline",
        #             "is_active": request.resolver_match.view_name == "predictions:predictions_web:index",
        #         },
        #     ]

        # guru
        # if has_group(request.user, ROLE_GURU):
        #     menus += [
        #         {
        #             "title": "Kelas",
        #             "url": "kelas:index",
        #         },
        #         {
        #             "title": "Tugas",
        #             "url": "tugas:index",
        #         },
        #     ]


    return {
        "sidebar_menus": menus
    }
    

def permissions(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user

    return {
        "roles": permission_service.get_roles(user),
    }