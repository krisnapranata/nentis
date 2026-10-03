from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from pendaftaran.models import Pendaftaran
from resep.forms import ResepDetailFormSet
from resep.models import MasterObat, Resep


def is_dokter(user):
    return user.role in ('dokter', 'admin')


def is_admisi(user):
    return user.role in ('admisi', 'admin')


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
def cari_obat(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 3:
        return JsonResponse({'results': []})
    obats = MasterObat.objects.filter(is_active=True, nama__icontains=q)[:20]
    return JsonResponse({
        'results': [{'id': o.id, 'nama': o.nama} for o in obats]
    })


@login_required
@user_passes_test(is_admisi, login_url='/accounts/login/')
def master_obat_list(request):
    if request.method == 'POST':
        nama = request.POST.get('nama', '').strip()
        dosis_default = request.POST.get('dosis_default', '').strip()
        satuan = request.POST.get('satuan', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        if nama:
            obat, created = MasterObat.objects.get_or_create(nama=nama)
            obat.dosis_default = dosis_default or None
            obat.satuan = satuan or None
            obat.is_active = is_active
            obat.save()
            if created:
                messages.success(request, f'Obat "{nama}" berhasil ditambahkan.')
            else:
                messages.info(request, f'Obat "{nama}" sudah ada, data diperbarui.')
            return redirect('admisi_master_obat')
        messages.error(request, 'Nama obat wajib diisi.')

    obats = MasterObat.objects.all().order_by('nama')
    return render(request, 'resep/master_obat.html', {'obats': obats})


@login_required
@user_passes_test(is_admisi, login_url='/accounts/login/')
def toggle_master_obat(request, obat_id):
    obat = get_object_or_404(MasterObat, id=obat_id)
    obat.is_active = not obat.is_active
    obat.save()
    state = 'diaktifkan' if obat.is_active else 'dinonaktifkan'
    messages.success(request, f'Obat "{obat.nama}" {state}.')
    return redirect('admisi_master_obat')


@login_required
@user_passes_test(is_admisi, login_url='/accounts/login/')
def master_obat_edit(request, obat_id):
    obat = get_object_or_404(MasterObat, id=obat_id)
    if request.method == 'POST':
        nama = request.POST.get('nama', '').strip()
        if not nama:
            messages.error(request, 'Nama obat wajib diisi.')
        else:
            obat.nama = nama
            obat.dosis_default = request.POST.get('dosis_default', '').strip() or None
            obat.satuan = request.POST.get('satuan', '').strip() or None
            obat.is_active = request.POST.get('is_active') == 'on'
            obat.save()
            messages.success(request, f'Obat "{nama}" berhasil diperbarui.')
            return redirect('admisi_master_obat')

    obats = MasterObat.objects.all().order_by('nama')
    return render(request, 'resep/master_obat.html', {'obats': obats, 'edit_obat': obat})


@login_required
@user_passes_test(is_admisi, login_url='/accounts/login/')
def master_obat_delete(request, obat_id):
    obat = get_object_or_404(MasterObat, id=obat_id)
    if request.method == 'POST':
        nama = obat.nama
        obat.delete()
        messages.success(request, f'Obat "{nama}" berhasil dihapus.')
    return redirect('admisi_master_obat')


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
def buat_resep(request, pendaftaran_id):
    pendaftaran = get_object_or_404(Pendaftaran, id=pendaftaran_id)
    resep = Resep.objects.filter(pendaftaran=pendaftaran).first()

    if request.method == 'POST':
        if not resep:
            resep = Resep.objects.create(
                pendaftaran=pendaftaran,
                dokter=request.user,
            )

        formset = ResepDetailFormSet(request.POST, instance=resep)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Resep berhasil disimpan.')
            return redirect('dokter_periksa', pendaftaran_id=pendaftaran.id)
        else:
            return render(request, 'resep/form.html', {
                'formset': formset, 'pendaftaran': pendaftaran, 'resep': resep
            })
    else:
        if not resep:
            resep = Resep.objects.create(
                pendaftaran=pendaftaran,
                dokter=request.user,
            )
        formset = ResepDetailFormSet(instance=resep)
        return render(request, 'resep/form.html', {
            'formset': formset, 'pendaftaran': pendaftaran, 'resep': resep
        })
