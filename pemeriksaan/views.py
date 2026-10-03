from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from antrian.models import Antrian
from pasien.models import Pasien
from pemeriksaan.forms import CPPTForm
from pemeriksaan.models import CPPT
from pendaftaran.models import KeadaanKhusus, Pendaftaran
from resep.models import Resep


def _today():
    return timezone.localtime(timezone.now()).date()


def is_dokter(user):
    return user.role in ('dokter', 'admin')


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
def dokter_dashboard(request):
    today = _today()
    context = {
        'menunggu': Pendaftaran.objects.filter(tanggal_kunjungan=today, status='MENUNGGU').count(),
        'dipanggil': Pendaftaran.objects.filter(tanggal_kunjungan=today, status='DIPANGGIL').count(),
        'diperiksa': Pendaftaran.objects.filter(tanggal_kunjungan=today, status='DIPERIKSA').count(),
        'selesai': Pendaftaran.objects.filter(tanggal_kunjungan=today, status='SELESAI').count(),
    }
    return render(request, 'pemeriksaan/dashboard.html', context)


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
def periksa_pasien(request, pendaftaran_id):
    pendaftaran = get_object_or_404(Pendaftaran, id=pendaftaran_id)
    pasien = pendaftaran.pasien

    antrian = getattr(pendaftaran, 'antrian', None)
    if antrian and antrian.status in ('MENUNGGU', 'DIPANGGIL'):
        antrian.status = 'DIPERIKSA'
        antrian.save()
        pendaftaran.status = 'DIPERIKSA'
        pendaftaran.save()

    riwayat_kunjungan = Pendaftaran.objects.filter(
        pasien=pasien
    ).exclude(id=pendaftaran_id).select_related('odontogram').prefetch_related('keadaan_khusus').order_by('-tanggal_kunjungan', '-waktu_daftar')[:10]

    cppt_list = CPPT.objects.filter(pendaftaran=pendaftaran).order_by('-tanggal_jam')
    riwayat_cppt = CPPT.objects.filter(pendaftaran__pasien=pasien).exclude(
        pendaftaran=pendaftaran
    ).select_related('pendaftaran').order_by('-tanggal_jam')[:10]

    resep = Resep.objects.filter(pendaftaran=pendaftaran).first()
    keadaan_khusus = KeadaanKhusus.objects.filter(pendaftaran=pendaftaran).first()

    pendaftaran_aktif = Pendaftaran.objects.filter(
        pasien=pasien
    ).exclude(status='SELESAI').order_by('-tanggal_kunjungan', '-waktu_daftar').first()

    keadaan_khusus_terakhir = None
    keadaan_khusus_terakhir_tanggal = None
    if not keadaan_khusus:
        kunjungan_sebelumnya = Pendaftaran.objects.filter(
            pasien=pasien
        ).exclude(id=pendaftaran_id).order_by('-tanggal_kunjungan', '-waktu_daftar')
        for k in kunjungan_sebelumnya:
            kk = KeadaanKhusus.objects.filter(pendaftaran=k).first()
            if kk:
                keadaan_khusus_terakhir = kk
                keadaan_khusus_terakhir_tanggal = k.tanggal_kunjungan
                break

    return render(request, 'pemeriksaan/periksa.html', {
        'pendaftaran': pendaftaran,
        'pasien': pasien,
        'antrian': antrian,
        'riwayat_kunjungan': riwayat_kunjungan,
        'cppt_list': cppt_list,
        'riwayat_cppt': riwayat_cppt,
        'resep': resep,
        'keadaan_khusus': keadaan_khusus,
        'keadaan_khusus_terakhir': keadaan_khusus_terakhir,
        'keadaan_khusus_terakhir_tanggal': keadaan_khusus_terakhir_tanggal,
        'pendaftaran_aktif': pendaftaran_aktif,
    })


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
def simpan_keadaan_khusus(request, pendaftaran_id):
    pendaftaran = get_object_or_404(Pendaftaran, id=pendaftaran_id)

    if request.method == 'POST':
        kk, _ = KeadaanKhusus.objects.get_or_create(pendaftaran=pendaftaran)

        hamil = request.POST.get('hamil') or None
        kk.hamil = hamil if hamil else None
        kk.hipertensi = request.POST.get('hipertensi') == '1'
        kk.hipertensi_keterangan = request.POST.get('hipertensi_keterangan', '') or None
        kk.riwayat_jantung = request.POST.get('riwayat_jantung') == '1'
        kk.riwayat_jantung_nama_dokter = request.POST.get('riwayat_jantung_nama_dokter', '') or None
        kk.alergi_obat = request.POST.get('alergi_obat') == '1'
        kk.alergi_obat_nama = request.POST.get('alergi_obat_nama', '') or None
        kk.keterangan = request.POST.get('keterangan', '') or None
        kk.save()

        messages.success(request, 'Keadaan khusus berhasil disimpan.')

    return redirect('dokter_periksa', pendaftaran_id=pendaftaran.id)


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
def buat_cppt(request, pendaftaran_id):
    pendaftaran = get_object_or_404(Pendaftaran, id=pendaftaran_id)
    if request.method == 'POST':
        form = CPPTForm(request.POST)
        if form.is_valid():
            cppt = form.save(commit=False)
            cppt.pendaftaran = pendaftaran
            cppt.dokter = request.user
            cppt.save()
            messages.success(request, 'Pemeriksaan berhasil disimpan.')
            return redirect('dokter_periksa', pendaftaran_id=pendaftaran.id)
    else:
        form = CPPTForm()
    return render(request, 'pemeriksaan/cppt_form.html', {
        'form': form, 'pendaftaran': pendaftaran
    })


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
def selesai_pelayanan(request, pendaftaran_id):
    pendaftaran = get_object_or_404(Pendaftaran, id=pendaftaran_id)

    cppt_ada = CPPT.objects.filter(pendaftaran=pendaftaran).exists()
    if not cppt_ada:
        messages.error(request, 'Pemeriksaan harus diisi sebelum menyelesaikan pelayanan.')
        return redirect('dokter_periksa', pendaftaran_id=pendaftaran.id)

    pendaftaran.status = 'SELESAI'
    pendaftaran.save()

    antrian = getattr(pendaftaran, 'antrian', None)
    if antrian:
        antrian.status = 'SELESAI'
        antrian.save()

    messages.success(request, 'Pelayanan selesai.')
    return redirect('dokter_dashboard')


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
def riwayat_pasien(request, pasien_id):
    pasien = get_object_or_404(Pasien, id=pasien_id)
    kunjungan_list = Pendaftaran.objects.filter(
        pasien=pasien
    ).select_related('odontogram').prefetch_related('keadaan_khusus').order_by('-tanggal_kunjungan', '-waktu_daftar')

    return render(request, 'pemeriksaan/riwayat.html', {
        'pasien': pasien,
        'kunjungan_list': kunjungan_list,
    })
