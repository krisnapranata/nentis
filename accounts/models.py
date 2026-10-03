from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('admisi', 'Petugas Admisi'),
        ('dokter', 'Dokter Gigi'),
        ('pasien', 'Pasien'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admisi')
    no_hp = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'accounts_user'
