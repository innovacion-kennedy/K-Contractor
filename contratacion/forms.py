from django import forms
from .models import Contrato, Documento, Convocatoria, EvaluacionHV
from .models import Funcionario

# Formulario para contrato (usa Funcionario en vez de Persona)


class ContratoForm(forms.ModelForm):
    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Contrato
        fields = '__all__'
        widgets = {
            'numero_contrato': forms.TextInput(attrs={'class': 'form-control'}),
            'proyecto': forms.TextInput(attrs={'class': 'form-control'}),
            'actividad': forms.Textarea(attrs={'class': 'form-control'}),
            'arl': forms.TextInput(attrs={'class': 'form-control'}),
            'eps': forms.TextInput(attrs={'class': 'form-control'}),
            'fondo_pensiones': forms.TextInput(attrs={'class': 'form-control'}),
            'sipse': forms.TextInput(attrs={'class': 'form-control'}),
            'cdp': forms.TextInput(attrs={'class': 'form-control'}),
            'objeto_contrato': forms.Textarea(attrs={'class': 'form-control'}),
            'honorarios': forms.NumberInput(attrs={'class': 'form-control'}),
            'duracion_meses': forms.NumberInput(attrs={'class': 'form-control'}),
            'modalidad_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'fuente_recurso': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_contrato': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_firma_contrato': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'supervisor_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'supervisor_cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'supervisor_correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'supervisor_telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'documento_rut': forms.TextInput(attrs={'class': 'form-control'}),
            'documento_cert_bancaria': forms.TextInput(attrs={'class': 'form-control'}),
            'documento_seguridad_social': forms.TextInput(attrs={'class': 'form-control'}),
            'documento_antecedentes': forms.TextInput(attrs={'class': 'form-control'}),
            'documento_poliza': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
        }

# Formulario para subir documentos


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ["tipo_documento", "archivo"]
        widgets = {
            "tipo_documento": forms.TextInput(attrs={"class": "form-control"}),
            "archivo": forms.FileInput(attrs={"class": "form-control"}),
        }

# Formulario para convocatoria


class ConvocatoriaForm(forms.ModelForm):
    class Meta:
        model = Convocatoria
        fields = ['titulo', 'descripcion', 'documento', 'estado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'documento': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario para evaluación de hoja de vida


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
        widgets = {
            'convocatoria': forms.Select(attrs={'class': 'form-control'}),
            'puntaje': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ❌ Formularios que ya no se usan, pero quedan comentados por si se necesitan más adelante:

# class SeguimientoContratoForm(forms.ModelForm):
#     class Meta:
#         model = SeguimientoContrato
#         fields = ['comentario']
#         widgets = {
#             'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         }

# class DocumentosContratoForm(forms.ModelForm):
#     class Meta:
#         model = DocumentosContrato
#         fields = ["tipo_documento", "archivo"]
#         widgets = {
#             "tipo_documento": forms.TextInput(attrs={"class": "form-control"}),
#             "archivo": forms.FileInput(attrs={"class": "form-control"}),
#         }
