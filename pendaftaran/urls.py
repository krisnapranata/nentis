from django.urls import path

from pendaftaran import views

urlpatterns = [
    path('', views.admisi_dashboard, name='admisi_dashboard'),
    path('pasien/', views.daftar_pasien, name='admisi_pasien'),
    path('pasien/baru/', views.pasien_baru, name='admisi_pasien_baru'),
    path('pendaftaran/<int:pasien_id>/', views.buat_kunjungan, name='admisi_buat_kunjungan'),
    path('checkin/<int:pendaftaran_id>/', views.admisi_checkin, name='admisi_checkin'),
    path('antrian/', views.admisi_antrian_list, name='admisi_antrian'),
]
