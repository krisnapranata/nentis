from io import BytesIO

import qrcode
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from antrian.models import Antrian
from pasien.forms import PasienForm
from pasien.models import Pasien
from pendaftaran.models import Pendaftaran


def _local_now():
    return timezone.localtime(timezone.now())


def _today():
    return _local_now().date()


def _generate_nomor_antrian():
    today = _today()
    last = Antrian.objects.filter(tanggal=today).order_by('-nomor_antrian').first()
    if last:
        try:
            num = int(last.nomor_antrian[1:]) + 1
        except (ValueError, IndexError):
            num = int(last.nomor_antrian) + 1
    else:
        num = 1
    return f'A{num:03d}'


def _lakukan_checkin(pendaftaran):
    today = _today()
    nomor = _generate_nomor_antrian()
    antrian = Antrian.objects.create(
        pendaftaran=pendaftaran,
        tanggal=today,
        nomor_antrian=nomor,
        waktu_checkin=timezone.now(),
        status='MENUNGGU',
    )
    pendaftaran.status = 'MENUNGGU'
    pendaftaran.save()
    return antrian


def generate_qr(url, request):
    full_url = request.build_absolute_uri(url)
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(full_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buf = BytesIO()
    img.save(buf, format='PNG')
    return HttpResponse(buf.getvalue(), content_type='image/png')


def qr_daftar(request):
    return generate_qr('/daftar/', request)


def qr_checkin(request):
    return generate_qr('/checkin/', request)


def qr_page(request):
    return render(request, 'pasien/qr_page.html')


def daftar(request):
    if request.method == 'POST':
        form = PasienForm(request.POST)
        no_ktp = request.POST.get('no_ktp', '').strip()
        no_hp = request.POST.get('no_hp', '').strip()
        nama = request.POST.get('nama_lengkap', '').strip()
        pasien = None

        if no_ktp:
            pasien = Pasien.objects.filter(no_ktp=no_ktp).first()
        if not pasien and no_hp:
            pasien = Pasien.objects.filter(no_hp=no_hp, nama_lengkap__iexact=nama).first()

        if not pasien and form.is_valid():
            pasien = form.save()

        if pasien:
            today = _today()
            existing = Pendaftaran.objects.filter(
                pasien=pasien, tanggal_kunjungan=today
            ).first()

            if existing:
                antrian = getattr(existing, 'antrian', None)
                if existing.status == 'TERDAFTAR':
                    antrian = _lakukan_checkin(existing)
                    existing.refresh_from_db()
                return render(request, 'pasien/daftar_sukses.html', {
                    'pasien': pasien,
                    'pendaftaran': existing,
                    'antrian': antrian,
                    'already_registered': True,
                })

            kode = f'REG-{_local_now():%Y%m%d}-{pasien.id:04d}'
            pendaftaran = Pendaftaran.objects.create(
                pasien=pasien,
                tanggal_kunjungan=today,
                cara_daftar='MANDIRI',
                kode_pendaftaran=kode,
                status='TERDAFTAR',
            )

            antrian = _lakukan_checkin(pendaftaran)

            return render(request, 'pasien/daftar_sukses.html', {
                'pasien': pasien,
                'pendaftaran': pendaftaran,
                'antrian': antrian,
            })

        messages.error(request, 'Nama dan No. HP wajib diisi.')
        return render(request, 'pasien/daftar.html', {'form': form})

    q = request.GET.get('query', '').strip()
    show_form = request.GET.get('baru') == '1'
    results = []
    searched = bool(q)

    if q:
        results = Pasien.objects.filter(
            Q(nama_lengkap__icontains=q) |
            Q(no_hp__icontains=q) |
            Q(no_ktp__icontains=q) |
            Q(alamat__icontains=q)
        )[:20]

    form = PasienForm()
    return render(request, 'pasien/daftar.html', {
        'form': form,
        'results': results,
        'searched': searched,
        'query': q,
        'show_form': show_form or (searched and not results),
    })


def checkin_public(request):
    if request.method == 'POST':
        kode = request.POST.get('kode_pendaftaran', '').strip()
        no_ktp = request.POST.get('no_ktp', '').strip()

        pendaftaran = None
        if kode:
            pendaftaran = Pendaftaran.objects.filter(
                kode_pendaftaran=kode, status='TERDAFTAR'
            ).first()
        elif no_ktp:
            pendaftaran = Pendaftaran.objects.filter(
                pasien__no_ktp=no_ktp, status='TERDAFTAR'
            ).order_by('-waktu_daftar').first()

        if pendaftaran:
            antrian = _lakukan_checkin(pendaftaran)
            return render(request, 'pasien/checkin_sukses.html', {
                'pendaftaran': pendaftaran,
                'antrian': antrian,
            })
        messages.error(request, 'Pendaftaran tidak ditemukan atau sudah check-in.')
        return render(request, 'pasien/checkin.html')

    return render(request, 'pasien/checkin.html')


def antrian_public(request, kode):
    pendaftaran = get_object_or_404(Pendaftaran, kode_pendaftaran=kode)
    antrian = getattr(pendaftaran, 'antrian', None)
    return render(request, 'pasien/antrian_status.html', {
        'pendaftaran': pendaftaran,
        'antrian': antrian,
    })
