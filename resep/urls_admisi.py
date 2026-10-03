from django.urls import path

from resep import views

urlpatterns = [
    path('master-obat/', views.master_obat_list, name='admisi_master_obat'),
    path('master-obat/toggle/<int:obat_id>/', views.toggle_master_obat, name='admisi_toggle_obat'),
    path('master-obat/edit/<int:obat_id>/', views.master_obat_edit, name='admisi_edit_obat'),
    path('master-obat/delete/<int:obat_id>/', views.master_obat_delete, name='admisi_delete_obat'),
]
