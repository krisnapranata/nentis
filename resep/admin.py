from django.contrib import admin

from resep.models import MasterObat, Resep, ResepDetail


class ResepDetailInline(admin.TabularInline):
    model = ResepDetail
    extra = 1


@admin.register(MasterObat)
class MasterObatAdmin(admin.ModelAdmin):
    list_display = ['nama', 'dosis_default', 'satuan', 'is_active']
    list_filter = ['is_active']
    search_fields = ['nama']


@admin.register(Resep)
class ResepAdmin(admin.ModelAdmin):
    list_display = ['pendaftaran', 'dokter', 'tanggal']
    search_fields = ['pendaftaran__pasien__nama_lengkap']
    inlines = [ResepDetailInline]
