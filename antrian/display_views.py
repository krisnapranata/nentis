from django.shortcuts import render
from django.utils import timezone

from antrian.models import Antrian


def _today():
    return timezone.localtime(timezone.now()).date()


def display_antrian(request):
    today = _today()
    antrian_list = Antrian.objects.filter(
        tanggal=today, status__in=['MENUNGGU', 'DIPANGGIL', 'DIPERIKSA']
    ).select_related('pendaftaran__pasien').order_by('nomor_antrian')

    dipanggil_list = Antrian.objects.filter(
        tanggal=today, status='DIPANGGIL'
    ).order_by('-waktu_dipanggil')

    return render(request, 'antrian/display.html', {
        'antrian_list': antrian_list,
        'dipanggil_list': dipanggil_list,
        'today': today,
    })


def display_rows(request):
    today = _today()
    antrian_list = Antrian.objects.filter(
        tanggal=today, status__in=['MENUNGGU', 'DIPANGGIL', 'DIPERIKSA']
    ).select_related('pendaftaran__pasien').order_by('nomor_antrian')

    dipanggil_list = Antrian.objects.filter(
        tanggal=today, status='DIPANGGIL'
    ).order_by('-waktu_dipanggil')

    return render(request, 'antrian/_display_rows.html', {
        'antrian_list': antrian_list,
        'dipanggil_list': dipanggil_list,
    })
