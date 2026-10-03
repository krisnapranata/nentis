from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from antrian.models import Antrian


def _today():
    return timezone.localtime(timezone.now()).date()


def is_admisi(user):
    return user.role in ('admisi', 'admin')


def is_dokter(user):
    return user.role in ('dokter', 'admin')


def is_petugas(user):
    return user.role in ('admisi', 'dokter', 'admin')


@login_required
@user_passes_test(is_petugas, login_url='/accounts/login/')
def panggil_antrian(request, antrian_id):
    antrian = get_object_or_404(Antrian, id=antrian_id, status__in=['MENUNGGU', 'DIPANGGIL'])
    antrian.status = 'DIPANGGIL'
    antrian.waktu_dipanggil = timezone.now()
    antrian.save()
    antrian.pendaftaran.status = 'DIPANGGIL'
    antrian.pendaftaran.save()
    messages.success(request, f'Pasien {antrian.nomor_antrian} dipanggil.')

    if request.headers.get('HX-Request'):
        today = _today()
        if request.user.role in ('admisi', 'admin'):
            antrian_list = Antrian.objects.filter(tanggal=today).select_related(
                'pendaftaran__pasien'
            ).order_by('status', 'nomor_antrian')
            return render(request, 'pendaftaran/_antrian_rows.html', {
                'menunggu': antrian_list.filter(status__in=['MENUNGGU', 'DIPANGGIL']),
                'diperiksa': antrian_list.filter(status='DIPERIKSA'),
                'selesai': antrian_list.filter(status='SELESAI'),
            })
        all_antrian = Antrian.objects.filter(tanggal=today).select_related(
            'pendaftaran__pasien'
        ).order_by('nomor_antrian')
        menunggu_list = [a for a in all_antrian if a.status in ('MENUNGGU', 'DIPANGGIL')]
        return render(request, 'antrian/_dokter_menunggu_rows.html', {
            'menunggu_list': menunggu_list,
        })

    if request.user.role in ('admisi', 'admin'):
        return redirect('admisi_antrian')
    return redirect('dokter_antrian')


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
def dokter_antrian_list(request):
    today = _today()
    all_antrian = Antrian.objects.filter(
        tanggal=today
    ).select_related('pendaftaran__pasien').order_by('nomor_antrian')

    menunggu_list = [a for a in all_antrian if a.status in ('MENUNGGU', 'DIPANGGIL')]
    diperiksa_list = [a for a in all_antrian if a.status == 'DIPERIKSA']
    selesai_list = [a for a in all_antrian if a.status == 'SELESAI']

    return render(request, 'antrian/dokter_antrian.html', {
        'menunggu_list': menunggu_list,
        'diperiksa_list': diperiksa_list,
        'selesai_list': selesai_list,
    })
