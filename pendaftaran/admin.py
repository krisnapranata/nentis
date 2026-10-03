from django.contrib import admin

from pendaftaran.models import KeadaanKhusus, Pendaftaran


@admin.register(Pendaftaran)
class PendaftaranAdmin(admin.ModelAdmin):
    list_display = ['kode_pendaftaran', 'pasien', 'tanggal_kunjungan', 'cara_daftar', 'status']
    list_filter = ['status', 'cara_daftar', 'tanggal_kunjungan']
    search_fields = ['kode_pendaftaran', 'pasien__nama_lengkap']


@admin.register(KeadaanKhusus)
class KeadaanKhususAdmin(admin.ModelAdmin):
    list_display = ['pendaftaran', 'hamil', 'hipertensi', 'riwayat_jantung', 'alergi_obat']
    search_fields = ['pendaftaran__pasien__nama_lengkap']
