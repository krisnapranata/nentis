from django import forms

from pemeriksaan.models import CPPT


class CPPTForm(forms.ModelForm):
    class Meta:
        model = CPPT
        fields = ['subjective', 'objective', 'assessment', 'plan']
        widgets = {
            'subjective': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Keluhan yang disampaikan pasien...'}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Temuan klinis, kondisi gigi dan mulut...'}),
            'assessment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Diagnosis atau kesimpulan...'}),
            'plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Rencana tindakan yang akan dilakukan...'}),
        }
