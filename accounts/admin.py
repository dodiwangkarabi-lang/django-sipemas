from django.contrib import admin

# models
from accounts.models import (
    Masyarakat, Petugas
)

# Register your models here.
admin.site.register(Masyarakat)
admin.site.register(Petugas)