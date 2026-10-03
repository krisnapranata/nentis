import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from odontogram.models import KONDISI_CHOICES, Odontogram, KondisiGigi
from pendaftaran.models import Pendaftaran


def is_dokter(user):
    return user.role in ('dokter', 'admin')


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
@ensure_csrf_cookie
def get_odontogram(request, pendaftaran_id):
    pendaftaran = get_object_or_404(Pendaftaran, id=pendaftaran_id)
    odontogram, created = Odontogram.objects.get_or_create(
        pendaftaran=pendaftaran,
        defaults={'dokter': request.user, 'jenis_gigi': 'PERMANEN'},
    )

    kondisi_map = odontogram.get_kondisi_map()
    data = {
        'id': odontogram.id,
        'jenis_gigi': odontogram.jenis_gigi,
        'kondisi': {str(k): v for k, v in kondisi_map.items()},
        'kondisi_choices': [{'value': c[0], 'label': c[1]} for c in KONDISI_CHOICES],
    }
    return JsonResponse(data)


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
@require_http_methods(['POST'])
def save_odontogram(request, pendaftaran_id):
    pendaftaran = get_object_or_404(Pendaftaran, id=pendaftaran_id)
    odontogram, created = Odontogram.objects.get_or_create(
        pendaftaran=pendaftaran,
        defaults={'dokter': request.user, 'jenis_gigi': 'PERMANEN'},
    )

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    jenis_gigi = body.get('jenis_gigi', odontogram.jenis_gigi)
    gigi_list = body.get('gigi', [])

    valid_jenis = ['PERMANEN', 'SULUNG']
    if jenis_gigi not in valid_jenis:
        return JsonResponse({'success': False, 'message': 'Jenis gigi tidak valid'}, status=400)

    odontogram.jenis_gigi = jenis_gigi
    odontogram.dokter = request.user
    odontogram.save()

    valid_conditions = [c[0] for c in KONDISI_CHOICES]

    for g in gigi_list:
        nomor = str(g.get('nomor', '')).strip()
        kondisi = g.get('kondisi', 'SEHAT')
        keterangan = g.get('keterangan', '')

        if not nomor or kondisi not in valid_conditions:
            continue

        KondisiGigi.objects.update_or_create(
            odontogram=odontogram,
            nomor_gigi=nomor,
            defaults={
                'kondisi': kondisi,
                'keterangan': keterangan,
            },
        )

    return JsonResponse({
        'success': True,
        'message': 'Odontogram berhasil disimpan.',
        'saved_count': len(gigi_list),
    })


@login_required
@user_passes_test(is_dokter, login_url='/accounts/login/')
@require_http_methods(['POST'])
def reset_odontogram(request, pendaftaran_id):
    pendaftaran = get_object_or_404(Pendaftaran, id=pendaftaran_id)
    odontogram = get_object_or_404(Odontogram, pendaftaran=pendaftaran)
    odontogram.kondisi.all().delete()

    return JsonResponse({
        'success': True,
        'message': 'Odontogram berhasil direset.',
    })
