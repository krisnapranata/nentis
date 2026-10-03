from django.urls import path

from pemeriksaan import views

urlpatterns = [
    path('', views.dokter_dashboard, name='dokter_dashboard'),
    path('periksa/<int:pendaftaran_id>/', views.periksa_pasien, name='dokter_periksa'),
    path('cppt/<int:pendaftaran_id>/', views.buat_cppt, name='dokter_cppt'),
    path('keadaan-khusus/<int:pendaftaran_id>/', views.simpan_keadaan_khusus, name='dokter_keadaan_khusus'),
    path('selesai/<int:pendaftaran_id>/', views.selesai_pelayanan, name='dokter_selesai'),
    path('riwayat/<int:pasien_id>/', views.riwayat_pasien, name='dokter_riwayat'),
]
