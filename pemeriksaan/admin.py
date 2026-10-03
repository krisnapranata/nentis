from django.contrib import admin

from pemeriksaan.models import CPPT


@admin.register(CPPT)
class CPPTAdmin(admin.ModelAdmin):
    list_display = ['pendaftaran', 'dokter', 'tanggal_jam']
    search_fields = ['pendaftaran__pasien__nama_lengkap', 'dokter__username']
