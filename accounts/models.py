from django.db import models
from django.contrib.auth.models import User

class Masyarakat(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='masyarakat'
    )

    nik = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    no_hp = models.CharField(max_length=20)
    
    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return f"{self.pk} {self.nama}"


class Petugas(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='petugas'
    )

    nama = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.pk} {self.nama}"

