from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from antrian.display_views import display_antrian, display_rows

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('pasien.urls')),
    path('display/', display_antrian, name='display_antrian'),
    path('display/rows/', display_rows, name='display_rows'),
    path('admisi/', include('pendaftaran.urls')),
    path('admisi/', include('antrian.urls_admisi')),
    path('admisi/', include('resep.urls_admisi')),
    path('dokter/', include('pemeriksaan.urls')),
    path('dokter/', include('antrian.urls_dokter')),
    path('dokter/', include('resep.urls')),
    path('dokter/', include('odontogram.urls')),
    path('dashboard/', include('dashboard.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
