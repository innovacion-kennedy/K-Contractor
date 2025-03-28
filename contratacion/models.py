from django.db import models
from login.models import Persona  # Importamos la clase existente
from django.conf import settings
import datetime


class Documento(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ("Hoja de Vida", "Hoja de Vida"),
        ("Cédula", "Cédula"),
        ("Certificación Mínima", "Certificación Mínima"),
    ]

    contratista = models.ForeignKey(
        Persona, on_delete=models.CASCADE, related_name="documentos"
    )
    tipo_documento = models.CharField(
        max_length=50, choices=TIPO_DOCUMENTO_CHOICES)
    archivo = models.FileField(upload_to="contratos/documentos/")
    estado = models.CharField(max_length=20, default="Pendiente")
    # ✅ Fecha automática al subir documento
    fecha_carga = models.DateTimeField(auto_now_add=True)
    # ✅ Fecha automática al modificar documento
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contratista.usuario.username} - {self.tipo_documento}"


class Contrato(models.Model):
    codigo_contrato = models.CharField(max_length=50, unique=True)
    numero_proyecto = models.CharField(max_length=50)
    nombre_proyecto = models.CharField(max_length=200)
    fecha_suscripcion = models.DateField()
    fecha_inicio = models.DateField()
    fecha_terminacion = models.DateField()
    valor_inicial_contrato = models.DecimalField(
        max_digits=12, decimal_places=2)
    valor_total_con_adiciones = models.DecimalField(
        max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Finalizado', 'Finalizado'),
    ], default='Pendiente')
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f"Contrato {self.codigo_contrato} - {self.nombre_proyecto}"


class DocumentosContrato(models.Model):
    # 🔹 Ahora vinculamos con el contratista
    contratista = models.ForeignKey(Persona, on_delete=models.CASCADE)
    contrato = models.ForeignKey(
        "Contrato", on_delete=models.CASCADE, null=True, blank=True)  # 🔹 Puede ser NULL
    tipo_documento = models.CharField(max_length=100)
    archivo = models.FileField(upload_to="contratos/documentos/")
    # 🔹 Estado inicial como "Pendiente"
    estado = models.CharField(max_length=20, default="Pendiente")
    fecha_subida = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo_documento} - {self.contratista.primer_nombre} {self.contratista.apellido_paterno}"


class SeguimientoContrato(models.Model):
    contrato = models.ForeignKey(
        Contrato, on_delete=models.CASCADE, related_name="seguimientos")
    comentario = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Seguimiento {self.contrato.codigo_contrato} - {self.fecha_registro}"


class Convocatoria(models.Model):
    ESTADOS = [
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada'),
        ('En evaluación', 'En evaluación'),
    ]

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    documento = models.FileField(
        upload_to='convocatorias/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(
        auto_now_add=True)  # ✅ Fecha automática
    estado = models.CharField(
        max_length=20, choices=ESTADOS, default='Abierta')
    creada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} - {self.estado}"


class EvaluacionHV(models.Model):
    ESTADOS = [
        ("Pendiente", "Pendiente"),
        ("Aprobado", "Aprobado"),
        ("Rechazado", "Rechazado"),
    ]

    contratista = models.ForeignKey(
        Persona, on_delete=models.CASCADE, related_name="evaluaciones"
    )
    convocatoria = models.ForeignKey(
        Convocatoria, on_delete=models.CASCADE, related_name="evaluaciones", null=True, blank=True
    )
    evaluador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    puntaje = models.IntegerField(default=0)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=10, choices=ESTADOS, default="Pendiente"
    )
    fecha_evaluacion = models.DateTimeField(
        auto_now_add=True)  # 📌 Fecha de evaluación
    fecha_asociacion = models.DateTimeField(
        null=True, blank=True)  # ✅ Nueva fecha de asociación

    def save(self, *args, **kwargs):
        """📌 Si la evaluación es nueva, asignamos la fecha de asociación automáticamente."""
        if not self.fecha_asociacion:
            self.fecha_asociacion = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Evaluación de {self.contratista.primer_nombre} ({self.estado})"
