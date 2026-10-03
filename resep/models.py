from django.conf import settings
from django.db import models

from pendaftaran.models import Pendaftaran


class MasterObat(models.Model):
    nama = models.CharField(max_length=200)
    dosis_default = models.CharField(max_length=100, blank=True, null=True)
    satuan = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_obat'
        ordering = ['nama']

    def __str__(self):
        return self.nama


class Resep(models.Model):
    pendaftaran = models.OneToOneField(Pendaftaran, on_delete=models.CASCADE, related_name='resep')
    dokter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tanggal = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resep'

    def __str__(self):
        return f'Resep {self.pendaftaran.pasien.nama_lengkap} - {self.tanggal:%d-%m-%Y}'


class ResepDetail(models.Model):
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE, related_name='detail')
    obat = models.ForeignKey(MasterObat, on_delete=models.CASCADE, blank=True, null=True)
    jumlah = models.CharField(max_length=50, blank=True, null=True)
    aturan_pakai = models.TextField()
    keterangan = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'resep_detail'

    def __str__(self):
        return self.obat.nama if self.obat else '-'
