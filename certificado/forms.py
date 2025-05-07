from django import forms
from django.contrib.auth.models import Group
from .models import Funcionario

class RegistroForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Seleccionar Rol",
        empty_label="Selecciona un grupo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Funcionario
        fields = ['primer_nombre', 'no_identificacion', 'CPS', 'sitio_expedicion', 'objeto', 'obligaciones', 'vr_inicial_contrato', 
                  'valor_mensual_honorarios', 'fecha_suscripcion', 'fecha_inicio', 'fecha_terminacion', 
                  'tiempo_ejecucion_dia', 'año_contrato', 'radicado']
        widgets = {
            'fecha_suscripcion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_terminacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }