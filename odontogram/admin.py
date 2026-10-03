from django.contrib import admin

from odontogram.models import Odontogram, KondisiGigi


class KondisiGigiInline(admin.TabularInline):
    model = KondisiGigi
    extra = 0


@admin.register(Odontogram)
class OdontogramAdmin(admin.ModelAdmin):
    list_display = ('pendaftaran', 'dokter', 'jenis_gigi', 'created_at')
    list_filter = ('jenis_gigi', 'created_at')
    search_fields = ('pendaftaran__pasien__nama_lengkap',)
    inlines = [KondisiGigiInline]
