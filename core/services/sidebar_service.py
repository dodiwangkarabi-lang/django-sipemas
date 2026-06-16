# apps/core/services/sidebar_service.py

def get_sidebar_menu(user):

    if not user.is_authenticated:
        return []

    menus = [
        {"title": "Dashboard", "url": "dashboard:index"},
    ]

    if user.groups.filter(name="Admin").exists():
        menus += [
            {"title": "Users", "url": "accounts:user_list"},
            {"title": "Settings", "url": "settings:index"},
        ]

    if user.groups.filter(name="Dosen").exists():
        menus += [
            {"title": "Kelas", "url": "kelas:index"},
            {"title": "Tugas", "url": "tugas:index"},
        ]

    if user.groups.filter(name="Mahasiswa").exists():
        menus += [
            {"title": "Pengumpulan Tugas", "url": "tugas:submit"},
        ]

    return menus