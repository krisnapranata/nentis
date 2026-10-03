from django.urls import path

from antrian import views

urlpatterns = [
    path('antrian/', views.dokter_antrian_list, name='dokter_antrian'),
    path('antrian/panggil/<int:antrian_id>/', views.panggil_antrian, name='dokter_panggil_antrian'),
]
