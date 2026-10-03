from django.urls import path

from resep import views

urlpatterns = [
    path('resep/cari-obat/', views.cari_obat, name='dokter_cari_obat'),
    path('resep/<int:pendaftaran_id>/', views.buat_resep, name='dokter_resep'),
]
