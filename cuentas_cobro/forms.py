from django import forms
from .models import CuentaCobro


class CuentaCobroForm(forms.ModelForm):
    class Meta:
        model = CuentaCobro
        fields = '__all__'
        widgets = {
            'numero_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_emision': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'valor_cobrado': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
