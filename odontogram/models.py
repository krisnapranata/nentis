from django.conf import settings
from django.db import models

from pendaftaran.models import Pendaftaran


JENIS_GIGI_CHOICES = (
    ('PERMANEN', 'Gigi Permanen'),
    ('SULUNG', 'Gigi Sulung'),
)

KONDISI_CHOICES = (
    ('SEHAT', 'Sehat / OK'),
    ('KARIES', 'Karies'),
    ('TUMPATAN', 'Tumpatan / Tambalan'),
    ('HILANG', 'Hilang / Dicabut'),
    ('MAHKOTA', 'Mahkota / Bridge'),
    ('RCT', 'Perawatan Saluran Akar (RCT)'),
    ('INDIKASI_CABUT', 'Indikasi Cabut'),
    ('PROTESA', 'Protesa / Gigi Palsu'),
)

WARNA_KONDISI = {
    'SEHAT': '#ffffff',
    'KARIES': '#dc3545',
    'TUMPATAN': '#0d6efd',
    'HILANG': '#212529',
    'MAHKOTA': '#ffc107',
    'RCT': '#fd7e14',
    'INDIKASI_CABUT': '#dc3545',
    'PROTESA': '#6f42c1',
}

PERMANEN_UPPER = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
PERMANEN_LOWER = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38]
SULUNG_UPPER = [55, 54, 53, 52, 51, 61, 62, 63, 64, 65]
SULUNG_LOWER = [85, 84, 83, 82, 81, 71, 72, 73, 74, 75]


class Odontogram(models.Model):
    pendaftaran = models.OneToOneField(
        Pendaftaran,
        on_delete=models.CASCADE,
        related_name='odontogram',
    )
    dokter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    jenis_gigi = models.CharField(max_length=10, choices=JENIS_GIGI_CHOICES, default='PERMANEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'odontogram'
        ordering = ['-created_at']

    def __str__(self):
        return f'Odontogram {self.pendaftaran.pasien.nama_lengkap} - {self.get_jenis_gigi_display()}'

    def get_kondisi_map(self):
        return {k.nomor_gigi: k.kondisi for k in self.kondisi.all()}


class KondisiGigi(models.Model):
    odontogram = models.ForeignKey(Odontogram, on_delete=models.CASCADE, related_name='kondisi')
    nomor_gigi = models.CharField(max_length=5)
    kondisi = models.CharField(max_length=20, choices=KONDISI_CHOICES, default='SEHAT')
    keterangan = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'kondisi_gigi'
        unique_together = ('odontogram', 'nomor_gigi')
        ordering = ['nomor_gigi']

    def __str__(self):
        return f'Gigi {self.nomor_gigi}: {self.get_kondisi_display()}'
