from django import template
from django.utils.safestring import mark_safe

from odontogram.models import WARNA_KONDISI, KONDISI_CHOICES

register = template.Library()

TOOTH_LABELS = dict(KONDISI_CHOICES)


@register.filter
def kondisi_map(odontogram):
    if not odontogram:
        return {}
    return odontogram.get_kondisi_map()


@register.filter
def ringkasan_kondisi(odontogram):
    if not odontogram:
        return []
    from collections import Counter
    k_map = odontogram.get_kondisi_map()
    counts = Counter(k_map.values())
    result = []
    wanted = ['KARIES', 'TUMPATAN', 'HILANG', 'MAHKOTA', 'RCT', 'INDIKASI_CABUT', 'PROTESA']
    for k in wanted:
        if counts.get(k, 0) > 0:
            result.append({
                'kondisi': k,
                'label': TOOTH_LABELS.get(k, k),
                'warna': WARNA_KONDISI.get(k, '#ccc'),
                'jumlah': counts[k],
            })
    sehat = counts.get('SEHAT', 0)
    if result:
        total = sum([r['jumlah'] for r in result])
        counted = total + sehat
    else:
        total = 0
    return result


@register.simple_tag
def mini_tooth_svg(odontogram):
    if not odontogram:
        return ''

    k_map = odontogram.get_kondisi_map()

    if odontogram.jenis_gigi == 'PERMANEN':
        upper = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
        lower = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38]
        tw = 18
        gap = 2
    else:
        upper = [55, 54, 53, 52, 51, 61, 62, 63, 64, 65]
        lower = [85, 84, 83, 82, 81, 71, 72, 73, 74, 75]
        tw = 22
        gap = 2

    th = 28
    parts = []

    def draw_row(teeth, y_offset):
        x = 4
        for n in teeth:
            kondisi = k_map.get(str(n), 'SEHAT')
            color = WARNA_KONDISI.get(kondisi, '#f8f9fa')
            text_color = '#fff' if kondisi not in ('SEHAT', 'MAHKOTA') else '#495057'
            rx = 2

            parts.append(
                f'<rect x="{x}" y="{y_offset}" width="{tw}" height="{th}" rx="{rx}" '
                f'fill="{color}" stroke="#adb5bd" stroke-width="0.5"/>'
            )

            if kondisi == 'HILANG' or kondisi == 'INDIKASI_CABUT':
                parts.append(
                    f'<line x1="{x+2}" y1="{y_offset+2}" x2="{x+tw-2}" y2="{y_offset+th-2}" '
                    f'stroke="#fff" stroke-width="1.5"/>'
                )
                parts.append(
                    f'<line x1="{x+tw-2}" y1="{y_offset+2}" x2="{x+2}" y2="{y_offset+th-2}" '
                    f'stroke="#fff" stroke-width="1.5"/>'
                )

            fs = '8' if odontogram.jenis_gigi == 'PERMANEN' else '9'
            parts.append(
                f'<text x="{x + tw/2}" y="{y_offset + th/2 + 1}" text-anchor="middle" '
                f'dominant-baseline="central" font-size="{fs}" font-weight="600" '
                f'fill="{text_color}">{n}</text>'
            )

            x += tw + gap

    draw_row(upper, 10)
    draw_row(lower, 50)

    return mark_safe('\n'.join(parts))
