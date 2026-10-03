from django.urls import path

from odontogram import views

urlpatterns = [
    path('odontogram/<int:pendaftaran_id>/', views.get_odontogram, name='dokter_odontogram_get'),
    path('odontogram/<int:pendaftaran_id>/save/', views.save_odontogram, name='dokter_odontogram_save'),
    path('odontogram/<int:pendaftaran_id>/reset/', views.reset_odontogram, name='dokter_odontogram_reset'),
]
