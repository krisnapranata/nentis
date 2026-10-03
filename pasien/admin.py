from django.contrib import admin

from pasien.models import Pasien


@admin.register(Pasien)
class PasienAdmin(admin.ModelAdmin):
    list_display = ['nama_lengkap', 'no_hp', 'no_ktp', 'created_at']
    search_fields = ['nama_lengkap', 'no_hp', 'no_ktp']
