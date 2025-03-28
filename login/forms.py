from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Persona


class RegistroForm(UserCreationForm):
    """
    Formulario de registro de usuario con opción de solicitar permiso especial.
    """
    email = forms.EmailField(required=True, label="Correo Electrónico")
    solicita_permiso_especial = forms.BooleanField(
        required=False, label="Pedir permisos especiales", initial=False
    )

    class Meta:
        model = Usuario
        fields = ["username", "email", "password1",
                  "password2", "solicita_permiso_especial"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.solicita_permiso_especial = self.cleaned_data["solicita_permiso_especial"]

        if commit:
            user.save()
        return user


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            "primer_nombre", "segundo_nombre", "apellido_paterno", "apellido_materno",
            "no_identificacion", "direccion", "telefono", "fecha_nacimiento",
            "nivel_formacion", "profesion", "eps", "fondo_pensiones", "solicita_permiso_especial",
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
