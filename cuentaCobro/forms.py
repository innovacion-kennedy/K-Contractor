from django import forms
from .models import CuentaCobro
from contratacion.models import Contrato
from login.models import Persona

class CuentaCobroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        
        if user:
            try:
                persona = Persona.objects.get(usuario=user)
                self.fields['contrato'].queryset = Contrato.objects.filter(persona=persona)
            except Persona.DoesNotExist:
                self.fields['contrato'].queryset = Contrato.objects.none()

    class Meta:
        model = CuentaCobro
        fields = ['contrato', 'numero_cuenta', 'estado', 'fecha_presentacion', 
                'nombre_contratista', 'tipo_identificacion_contratista', 
                'numero_identificacion_contratista', 'banco', 'tipo_cuenta', 
                'numero_cuenta_bancaria', 'valor_total']
        widgets = {
            'contrato': forms.Select(attrs={'class': 'form-control'}),
            'numero_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_presentacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nombre_contratista': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_identificacion_contratista': forms.Select(attrs={'class': 'form-control'}),
            'numero_identificacion_contratista': forms.TextInput(attrs={'class': 'form-control'}),
            'banco': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_cuenta': forms.Select(attrs={'class': 'form-control'}),
            'numero_cuenta_bancaria': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }
