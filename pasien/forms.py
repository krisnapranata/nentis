from django import forms

from pasien.models import Pasien


class PasienForm(forms.ModelForm):
    class Meta:
        model = Pasien
        fields = ['nama_lengkap', 'alamat', 'no_hp', 'no_ktp']
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'no_ktp': forms.TextInput(attrs={'class': 'form-control'}),
        }
