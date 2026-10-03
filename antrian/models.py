from django.db import models

from pendaftaran.models import Pendaftaran


class Antrian(models.Model):
    STATUS_CHOICES = [
        ('MENUNGGU', 'Menunggu'),
        ('DIPANGGIL', 'Dipanggil'),
        ('DIPERIKSA', 'Diperiksa'),
        ('SELESAI', 'Selesai'),
    ]

    pendaftaran = models.OneToOneField(Pendaftaran, on_delete=models.CASCADE, related_name='antrian')
    tanggal = models.DateField()
    nomor_antrian = models.CharField(max_length=10)
    waktu_checkin = models.DateTimeField()
    waktu_dipanggil = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='MENUNGGU')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'antrian'
        ordering = ['tanggal', 'nomor_antrian']
        unique_together = [['tanggal', 'nomor_antrian']]

    def __str__(self):
        return f'{self.nomor_antrian} - {self.pendaftaran.pasien.nama_lengkap}'
