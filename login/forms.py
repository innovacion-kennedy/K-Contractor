from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Persona
from django.contrib.auth.forms import PasswordChangeForm


class RegistroForm(UserCreationForm):
    """
    Formulario de registro de usuario sin solicitud de permiso especial.
    """
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = Usuario
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            "primer_nombre", "segundo_nombre", "apellido_paterno", "apellido_materno",
            "no_identificacion", "direccion", "telefono", "fecha_nacimiento", "rol",
            "nivel_formacion",
        ]
        labels = {
            'apellido_paterno': 'Primer Apellido',
            'apellido_materno': 'Segundo Apellido',
        }
        widgets = {
            'primer_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primer Nombre'}),
            'segundo_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Segundo Nombre'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primer Apellido'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Segundo Apellido'}),
            'no_identificacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Identificación'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }


class PersonaFormCompleto(forms.ModelForm):
    class Meta:
        model = Persona
        # Eliminados: 'solicita_permiso_especial', 'permiso_aprobado'
        exclude = ['usuario', 'rol']

        widgets = {
            # Textos y fechas
            'primer_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'segundo_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'no_identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_expedicion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_secundario': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),
            'institucion': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresos_mensuales': forms.TextInput(attrs={'class': 'form-control'}),
            'enfermedades_cronicas': forms.TextInput(attrs={'class': 'form-control'}),

            # Selects (FK o choices)
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'lugar_nacimiento': forms.Select(attrs={'class': 'form-control'}),
            'sexo_biologico': forms.Select(attrs={'class': 'form-control'}),
            'identidad_genero': forms.Select(attrs={'class': 'form-control'}),
            'orientacion_sexual': forms.Select(attrs={'class': 'form-control'}),
            'grupo_etnico': forms.Select(attrs={'class': 'form-control'}),
            'tipo_discapacidad': forms.Select(attrs={'class': 'form-control'}),
            'municipio_residencia': forms.Select(attrs={'class': 'form-control'}),
            'nivel_formacion': forms.Select(attrs={'class': 'form-control'}),
            'profesion': forms.Select(attrs={'class': 'form-control'}),
            'sector_economico': forms.Select(attrs={'class': 'form-control'}),
            'tipo_vivienda': forms.Select(attrs={'class': 'form-control'}),
            'zona': forms.Select(attrs={'class': 'form-control'}),
            'tipo_construccion': forms.Select(attrs={'class': 'form-control'}),
            'afiliacion_salud': forms.Select(attrs={'class': 'form-control'}),
            'acceso_servicios_salud': forms.Select(attrs={'class': 'form-control'}),

            # Booleanos
            'pertenencia_lgbti': forms.CheckboxInput(),
            'discapacidad': forms.CheckboxInput(),
            'victima_conflicto': forms.CheckboxInput(),
            'migrante': forms.CheckboxInput(),
            'poblacion_rural': forms.CheckboxInput(),
            'actualmente_estudia': forms.CheckboxInput(),
            'acceso_internet': forms.CheckboxInput(),

            # Números
            'estrato_social': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_personas_hogar': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña actual'
        })
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa la nueva contraseña'
        })
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma la nueva contraseña'
        })
    )
