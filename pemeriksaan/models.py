from django.conf import settings
from django.db import models

from pendaftaran.models import Pendaftaran


class CPPT(models.Model):
    pendaftaran = models.ForeignKey(Pendaftaran, on_delete=models.CASCADE, related_name='cppt')
    dokter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tanggal_jam = models.DateTimeField(auto_now_add=True)
    subjective = models.TextField()
    objective = models.TextField()
    assessment = models.TextField()
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cppt'
        ordering = ['-tanggal_jam']

    def __str__(self):
        return f'CPPT {self.pendaftaran.pasien.nama_lengkap} - {self.tanggal_jam:%d-%m-%Y %H:%M}'
