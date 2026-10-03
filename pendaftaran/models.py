from django.db import models

from pasien.models import Pasien


class Pendaftaran(models.Model):
    CARA_CHOICES = [
        ('ONLINE', 'Online'),
        ('ADMISI', 'Admisi'),
        ('MANDIRI', 'Mandiri'),
    ]
    STATUS_CHOICES = [
        ('TERDAFTAR', 'Terdaftar'),
        ('MENUNGGU', 'Menunggu'),
        ('DIPANGGIL', 'Dipanggil'),
        ('DIPERIKSA', 'Diperiksa'),
        ('SELESAI', 'Selesai'),
    ]

    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE, related_name='pendaftaran')
    tanggal_kunjungan = models.DateField()
    waktu_daftar = models.DateTimeField(auto_now_add=True)
    cara_daftar = models.CharField(max_length=10, choices=CARA_CHOICES, default='ONLINE')
    kode_pendaftaran = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TERDAFTAR')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pendaftaran'
        ordering = ['-waktu_daftar']

    def __str__(self):
        return f'{self.kode_pendaftaran} - {self.pasien.nama_lengkap}'


class KeadaanKhusus(models.Model):
    TRIMESTER_CHOICES = [
        ('TR1', 'Trimester 1'),
        ('TR2', 'Trimester 2'),
        ('TR3', 'Trimester 3'),
    ]

    pendaftaran = models.OneToOneField(
        Pendaftaran, on_delete=models.CASCADE, related_name='keadaan_khusus'
    )
    hamil = models.CharField(max_length=3, choices=TRIMESTER_CHOICES, blank=True, null=True)
    hipertensi = models.BooleanField(default=False)
    hipertensi_keterangan = models.TextField(blank=True, null=True)
    riwayat_jantung = models.BooleanField(default=False)
    riwayat_jantung_nama_dokter = models.CharField(max_length=200, blank=True, null=True)
    alergi_obat = models.BooleanField(default=False)
    alergi_obat_nama = models.CharField(max_length=200, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'keadaan_khusus'

    def __str__(self):
        return f'Keadaan Khusus - {self.pendaftaran.pasien.nama_lengkap}'
