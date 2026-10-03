from django.db import models


class Pasien(models.Model):
    nama_lengkap = models.CharField(max_length=200)
    alamat = models.TextField(blank=True, null=True)
    no_hp = models.CharField(max_length=20)
    no_ktp = models.CharField(max_length=30, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pasien'
        ordering = ['-created_at']

    def __str__(self):
        return self.nama_lengkap
