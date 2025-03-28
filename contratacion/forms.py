from django import forms
from .models import Contrato, DocumentosContrato, SeguimientoContrato, Documento, Convocatoria, EvaluacionHV


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = '__all__'
        widgets = {
            'codigo_contrato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese código único'}),
            'numero_proyecto': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_proyecto': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_suscripcion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_terminacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'valor_inicial_contrato': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_total_con_adiciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'persona': forms.Select(attrs={'class': 'form-control'}),
        }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ["tipo_documento", "archivo"]
        widgets = {
            "tipo_documento": forms.Select(attrs={"class": "form-control"}),
            "archivo": forms.FileInput(attrs={"class": "form-control"}),
        }


class SeguimientoContratoForm(forms.ModelForm):
    class Meta:
        model = SeguimientoContrato
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ["tipo_documento", "archivo"]
        widgets = {
            "tipo_documento": forms.Select(attrs={"class": "form-control"}),
            "archivo": forms.FileInput(attrs={"class": "form-control"}),
        }


class ConvocatoriaForm(forms.ModelForm):
    class Meta:
        model = Convocatoria
        fields = ['titulo', 'descripcion', 'documento', 'estado']


class EvaluacionHVForm(forms.ModelForm):
    class Meta:
        model = EvaluacionHV
        fields = ["convocatoria", "puntaje", "observaciones", "estado"]
        labels = {
            "convocatoria": "Convocatoria Evaluada",
            "puntaje": "Puntaje (0-100)",
            "observaciones": "Observaciones",
            "estado": "Estado de Evaluación",
        }
