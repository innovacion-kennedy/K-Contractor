from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from login.models import Persona
from contratacion.models import Contrato


class Cesion(models.Model):
    cedente = models.CharField(max_length=255, verbose_name="Cedente")
    cesionario = models.CharField(max_length=255, verbose_name="Cesionario")
    fecha_cesion = models.DateField(verbose_name="Fecha de Cesión")
    descripcion = models.TextField(
        blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return f"Cesion {self.id}: {self.cedente} -> {self.cesionario}"


def validar_fecha_terminacion(value):
    if value < timezone.now().date():
        raise ValidationError(
            "La fecha de terminación no puede ser en el pasado.")


class Funcionario(Persona):
    role = models.CharField(max_length=255, verbose_name="Rol o Cargo")
    CPS = models.CharField(max_length=255, verbose_name="CPS")
    sitio_expedicion = models.CharField(
        max_length=255, verbose_name="Sitio de Expedición")
    objeto = models.TextField(verbose_name="Objeto del Contrato")
    obligaciones = models.TextField(verbose_name="Obligaciones")
    vr_inicial_contrato = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor Inicial del Contrato")
    valor_mensual_honorarios = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor Mensual de Honorarios")
    fecha_suscripcion = models.DateField(verbose_name="Fecha de Suscripción")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_terminacion = models.DateField(
        verbose_name="Fecha de Terminación", validators=[validar_fecha_terminacion])
    tiempo_ejecucion_dia = models.IntegerField(
        verbose_name="Tiempo de Ejecución (Días)")
    año_contrato = models.IntegerField(verbose_name="Año del Contrato")
    radicado = models.CharField(max_length=255, verbose_name="Radicado")
    correo = models.EmailField(
        max_length=255, unique=True, default='correo@example.com')
    fecha_terminacion_prorrogas = models.DateField(
        null=True, blank=True, verbose_name="Fecha de Terminación de Prórrogas")
    plazo_total_ejecucion = models.IntegerField(
        null=True, blank=True, verbose_name="Plazo Total de Ejecución")
    cesion = models.ForeignKey(
        Cesion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cesión")
    suspensiones = models.TextField(
        null=True, blank=True, verbose_name="Suspensiones")
    estado = models.CharField(
        max_length=255,
        choices=[('activo', 'Activo'), ('terminado', 'Terminado')],
        default='terminado',
        verbose_name="Estado"
    )

    def __str__(self):
        return f"Funcionario: {self.primer_nombre} ({self.no_identificacion})"

    def esta_activo(self):
        return self.estado == 'activo'


class Radicado(models.Model):
    numero = models.CharField(
        max_length=255, unique=True, verbose_name="Número de Radicado")
    contrato = models.ForeignKey(
        Contrato, on_delete=models.CASCADE, related_name='radicados', verbose_name="Contrato")
    fecha_radicado = models.DateField(
        auto_now_add=True, verbose_name="Fecha de Radicado")
    descripcion = models.TextField(
        blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return f"Radicado {self.numero} - {self.contrato.codigo_contrato}"

    def año_radicado(self):
        return self.fecha_radicado.year
