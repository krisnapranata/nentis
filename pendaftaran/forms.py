from django import forms

from pendaftaran.models import Pendaftaran


class CariPasienForm(forms.Form):
    query = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cari nama / NIK / alamat / no HP...'})
    )


class PendaftaranAdmisiForm(forms.ModelForm):
    class Meta:
        model = Pendaftaran
        fields = ['cara_daftar']
        widgets = {
            'cara_daftar': forms.Select(attrs={'class': 'form-select'}),
        }
