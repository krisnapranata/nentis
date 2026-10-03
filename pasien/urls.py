from django.urls import path

from pasien import views

urlpatterns = [
    path('', views.qr_page, name='home'),
    path('daftar/', views.daftar, name='daftar'),
    path('checkin/', views.checkin_public, name='checkin'),
    path('antrian/<str:kode>/', views.antrian_public, name='antrian_public'),
    path('qrcode/daftar/', views.qr_daftar, name='qr_daftar'),
    path('qrcode/checkin/', views.qr_checkin, name='qr_checkin'),
]
