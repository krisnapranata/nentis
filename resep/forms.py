from django import forms

from resep.models import MasterObat, Resep, ResepDetail


class ResepDetailForm(forms.ModelForm):
    class Meta:
        model = ResepDetail
        fields = ['obat', 'jumlah', 'aturan_pakai', 'keterangan']
        widgets = {
            'obat': forms.Select(attrs={'class': 'form-control form-select'}),
            'jumlah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mis: 10'}),
            'aturan_pakai': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mis: 3x1 sebelum makan'}),
            'keterangan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mis: diminum sesudah makan'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['obat'].queryset = MasterObat.objects.filter(is_active=True)
        self.fields['obat'].empty_label = '-- Pilih Obat --'
        self.fields['obat'].required = True


ResepDetailFormSet = forms.inlineformset_factory(
    Resep, ResepDetail,
    form=ResepDetailForm,
    extra=1, can_delete=True
)

