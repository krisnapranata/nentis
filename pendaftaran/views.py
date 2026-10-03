from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from antrian.models import Antrian
from pasien.forms import PasienForm
from pasien.models import Pasien
from pendaftaran.forms import CariPasienForm
from pendaftaran.models import Pendaftaran


def _today():
    return timezone.localtime(timezone.now()).date()


def _local_now():
    return timezone.localtime(timezone.now())


def is_admisi(user):
    return user.role in ('admisi', 'admin')


@login_required
@user_passes_test(is_admisi, login_url='/accounts/login/')
def admisi_dashboard(request):
    today = _today()
    context = {
        'terdaftar': Pendaftaran.objects.filter(tanggal_kunjungan=today, status='TERDAFTAR').count(),
        'menunggu': Pendaftaran.objects.filter(tanggal_kunjungan=today, status='MENUNGGU').count(),
        'dipanggil': Pendaftaran.objects.filter(tanggal_kunjungan=today, status='DIPANGGIL').count(),
        'diperiksa': Pendaftaran.objects.filter(tanggal_kunjungan=today, status='DIPERIKSA').count(),
        'selesai': Pendaftaran.objects.filter(tanggal_kunjungan=today, status='SELESAI').count(),
    }
    return render(request, 'pendaftaran/dashboard.html', context)


@login_required
@user_passes_test(is_admisi, login_url='/accounts/login/')
def daftar_pasien(request):
    searched = False
    show_form = False
    pasien_form = PasienForm()

    if request.method == 'POST':
        pasien_form = PasienForm(request.POST)
        if pasien_form.is_valid():
            pasien = pasien_form.save()
            messages.success(request, f'Pasien baru "{pasien.nama_lengkap}" berhasil ditambahkan.')
            return redirect('admisi_buat_kunjungan', pasien_id=pasien.id)
        show_form = True
        qs = Pasien.objects.none()
    else:
        q = request.GET.get('query', '').strip()
        qs = Pasien.objects.all().order_by('-id')
        if q:
            searched = True
            qs = qs.filter(
                Q(nama_lengkap__icontains=q) |
                Q(no_hp__icontains=q) |
                Q(no_ktp__icontains=q) |
                Q(alamat__icontains=q)
            )
            if not qs.exists():
                show_form = True

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    form = CariPasienForm(request.GET or None)
    return render(request, 'pendaftaran/daftar_pasien.html', {
        'form': form,
        'page_obj': page_obj,
        'pasien_form': pasien_form,
        'searched': searched,
        'show_form': show_form,
    })


@login_required
@user_passes_test(is_admisi, login_url='/accounts/login/')
def pasien_baru(request):
    if request.method == 'POST':
        form = PasienForm(request.POST)
        if form.is_valid():
            pasien = form.save()
            return redirect('admisi_buat_kunjungan', pasien_id=pasien.id)
        return render(request, 'pendaftaran/pasien_form.html', {'form': form, 'title': 'Pasien Baru'})
    form = PasienForm()
    return render(request, 'pendaftaran/pasien_form.html', {'form': form, 'title': 'Pasien Baru'})


@login_required
@user_passes_test(is_admisi, login_url='/accounts/login/')
def buat_kunjungan(request, pasien_id):
    pasien = get_object_or_404(Pasien, id=pasien_id)
    today = _today()
    existing = Pendaftaran.objects.filter(
        pasien=pasien, tanggal_kunjungan=today
    ).first()

    if existing:
        if existing.status != 'SELESAI':
            messages.warning(request, f'{pasien.nama_lengkap} sudah terdaftar hari ini ({existing.get_status_display()}).')
            return redirect('admisi_checkin', pendaftaran_id=existing.id)
        messages.info(request, f'{pasien.nama_lengkap} sudah selesai diperiksa hari ini. Membuat kunjungan baru.')

    if request.method == 'POST':
        kode = f'ADM-{_local_now():%Y%m%d}-{pasien.id:04d}-{_local_now():%H%M%S}'
        pendaftaran = Pendaftaran.objects.create(
            pasien=pasien,
            tanggal_kunjungan=today,
            cara_daftar='ADMISI',
            kode_pendaftaran=kode,
            status='TERDAFTAR',
        )
        return redirect('admisi_checkin', pendaftaran_id=pendaftaran.id)

    if existing:
        return redirect('admisi_checkin', pendaftaran_id=existing.id)

    return render(request, 'pendaftaran/buat_kunjungan.html', {'pasien': pasien})


@login_required
@user_passes_test(is_admisi, login_url='/accounts/login/')
def admisi_checkin(request, pendaftaran_id):
    pendaftaran = get_object_or_404(Pendaftaran, id=pendaftaran_id)
    if pendaftaran.status != 'TERDAFTAR':
        messages.error(request, 'Pasien sudah check-in.')
        return redirect('admisi_antrian')

    today = _today()
    last = Antrian.objects.filter(tanggal=today).order_by('-nomor_antrian').first()
    if last:
        try:
            num = int(last.nomor_antrian[1:]) + 1
        except (ValueError, IndexError):
            num = int(last.nomor_antrian) + 1
    else:
        num = 1
    nomor = f'A{num:03d}'

    antrian = Antrian.objects.create(
        pendaftaran=pendaftaran,
        tanggal=today,
        nomor_antrian=nomor,
        waktu_checkin=timezone.now(),
        status='MENUNGGU',
    )
    pendaftaran.status = 'MENUNGGU'
    pendaftaran.save()

    messages.success(request, f'Check-in berhasil. Nomor antrean: {nomor}')
    return redirect('admisi_antrian')


@login_required
@user_passes_test(is_admisi, login_url='/accounts/login/')
def admisi_antrian_list(request):
    today = _today()
    antrian_list = Antrian.objects.filter(tanggal=today).select_related(
        'pendaftaran__pasien'
    ).order_by('status', 'nomor_antrian')

    menunggu = antrian_list.filter(status__in=['MENUNGGU', 'DIPANGGIL'])
    diperiksa = antrian_list.filter(status='DIPERIKSA')
    selesai = antrian_list.filter(status='SELESAI')

    ctx = {
        'menunggu': menunggu,
        'diperiksa': diperiksa,
        'selesai': selesai,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'pendaftaran/_antrian_rows.html', ctx)
    return render(request, 'pendaftaran/antrian_list.html', ctx)
