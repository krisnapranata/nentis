from django.urls import path

from antrian import views

urlpatterns = [
    path('antrian/panggil/<int:antrian_id>/', views.panggil_antrian, name='panggil_antrian'),
]
