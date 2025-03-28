from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.conf import settings
import uuid


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    groups = models.ManyToManyField(
        Group, related_name="usuario_groups", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="usuario_permissions", blank=True)

    solicita_permiso_especial = models.BooleanField(
        default=False)  # Nuevo campo

    def __str__(self):
        return f"{self.username} - {'Solicitó acceso especial' if self.solicita_permiso_especial else 'Acceso normal'}"


class Persona(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil")
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50, blank=True, null=True)
    no_identificacion = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    nivel_formacion = models.CharField(max_length=100)
    profesion = models.CharField(max_length=100, blank=True, null=True)
    eps = models.CharField(max_length=100)
    fondo_pensiones = models.CharField(max_length=100)

    solicita_permiso_especial = models.BooleanField(
        default=False)  # ✅ Solicitud del usuario
    permiso_aprobado = models.BooleanField(
        default=False)  # ✅ Lo aprueba el administrador

    def __str__(self):
        return f"{self.primer_nombre} {self.apellido_paterno}"
