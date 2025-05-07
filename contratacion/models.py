from django.db import models
from django.apps import apps
from django.conf import settings
from django.utils import timezone
import datetime


def obtener_persona():
    # Obtener el modelo Persona de la aplicación 'login' de forma segura
    Persona = apps.get_model('login', 'Persona')

    # Aquí puedes hacer lo que necesites con el modelo Persona
    personas = Persona.objects.all()
    return personas


class Documento(models.Model):  # COMPLETO
    id = models.AutoField(primary_key=True, db_column='id')

    contratista = models.ForeignKey(
        'login.Persona',
        on_delete=models.CASCADE,
        related_name='documentos',
        db_column='contratista_id'
    )

    tipo_documento = models.CharField(max_length=100, db_column='tipo')
    archivo = models.TextField(db_column='archivo')
    estado = models.CharField(max_length=50, db_column='estado')

    fecha_carga = models.DateTimeField(
        auto_now_add=True, db_column='fecha_carga')
    fecha_modificacion = models.DateTimeField(
        auto_now=True, db_column='fecha_modificacion')

    class Meta:
        managed = True
        db_table = 'documento'

    def __str__(self):
        return f"Documento {self.id} - {self.tipo_documento}"


class Convocatoria(models.Model):  # COMPLETO
    ESTADOS = [
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada'),
        ('En evaluación', 'En evaluación'),
    ]

    titulo = models.CharField(max_length=255, db_column='titulo')
    descripcion = models.TextField(db_column='descripcion')
    documento = models.FileField(
        upload_to='convocatorias/', blank=True, null=True, db_column='documento')
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, db_column='fecha_creacion')
    estado = models.CharField(
        max_length=20, choices=ESTADOS, default='Abierta', db_column='estado')

    creada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='convocatorias_creadas',
        db_column='creada_por'  # ← ajuste aquí
    )

    class Meta:
        managed = True
        db_table = 'convocatoria'

    def __str__(self):
        return f"{self.titulo} - {self.estado}"


class EvaluacionHV(models.Model):  # COMPLETO

    id = models.AutoField(primary_key=True, db_column='id')

    contratista = models.ForeignKey(
        'login.Persona',
        on_delete=models.CASCADE,
        db_column='contratista_id',
        related_name='evaluaciones'
    )
    convocatoria = models.ForeignKey(
        'Convocatoria',
        on_delete=models.SET_NULL,
        null=True,
        db_column='convocatoria_id'
    )
    evaluador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        db_column='evaluador_id'
    )
    puntaje = models.IntegerField(db_column='puntaje')
    observaciones = models.TextField(
        blank=True, null=True, db_column='observaciones')
    estado = models.CharField(max_length=50, db_column='estado')
    fecha_evaluacion = models.DateTimeField(
        auto_now_add=True, db_column='fecha')
    fecha_asociacion = models.DateTimeField(
        null=True, blank=True, db_column='fecha_asociacion')

    class Meta:
        managed = True
        db_table = 'evaluacionhv'

    def __str__(self):
        return f"Evaluación #{self.id} - {self.estado}"


class Contrato(models.Model):  # COMPLETO
    id = models.AutoField(primary_key=True, db_column='id')

    funcionario = models.ForeignKey(
        'Funcionario', on_delete=models.DO_NOTHING,
        db_column='funcionario_id', related_name='contratos'
    )
    proyecto = models.CharField(
        max_length=255, db_column='proyecto', default='Proyecto X')
    actividad = models.TextField(db_column='actividad', blank=True, null=True)

    arl = models.CharField(max_length=100, db_column='arl', default='Positiva')
    eps = models.CharField(
        max_length=100, db_column='eps', default='Nueva EPS')
    fondo_pensiones = models.CharField(
        max_length=100, db_column='fondo_pensiones', default='Colpensiones')

    sipse = models.CharField(
        max_length=100, db_column='sipse', blank=True, null=True)
    cdp = models.CharField(
        max_length=100, db_column='cdp', blank=True, null=True)

    objeto_contrato = models.TextField(
        db_column='objeto_contrato', default='Por definir')
    honorarios = models.DecimalField(
        max_digits=14, decimal_places=2, db_column='honorarios', default=0.0)
    duracion_meses = models.IntegerField(db_column='duracion_meses', default=1)

    modalidad_pago = models.CharField(
        max_length=100, db_column='modalidad_pago', default='Mensual')
    fuente_recurso = models.CharField(
        max_length=100, db_column='fuente_recurso', default='Recursos propios')
    estado_contrato = models.CharField(
        max_length=100, db_column='estado_contrato', default='Pendiente')

    fecha_inicio = models.DateField(
        db_column='fecha_inicio', default=timezone.now)
    fecha_fin = models.DateField(db_column='fecha_fin', default=timezone.now)
    fecha_firma_contrato = models.DateField(
        db_column='fecha_firma_contrato', default=timezone.now)

    numero_contrato = models.CharField(
        max_length=100, db_column='numero_contrato', default='TEMP-0001')

    supervisor_nombre = models.CharField(
        max_length=255, db_column='supervisor_nombre', default='Supervisor X')
    supervisor_cargo = models.CharField(
        max_length=255, db_column='supervisor_cargo', default='Cargo X')
    supervisor_correo = models.EmailField(
        db_column='supervisor_correo', default='correo@example.com')
    supervisor_telefono = models.CharField(
        max_length=100, db_column='supervisor_telefono', default='123456789')

    documento_rut = models.CharField(
        max_length=255, db_column='documento_rut', default='rut.pdf')
    documento_cert_bancaria = models.CharField(
        max_length=255, db_column='documento_cert_bancaria', default='cert_bancaria.pdf')
    documento_seguridad_social = models.CharField(
        max_length=255, db_column='documento_seguridad_social', default='seg_social.pdf')
    documento_antecedentes = models.CharField(
        max_length=255, db_column='documento_antecedentes', default='antecedentes.pdf')
    documento_poliza = models.CharField(
        max_length=255, db_column='documento_poliza', default='poliza.pdf')

    observaciones = models.TextField(
        db_column='observaciones', blank=True, null=True)

    usuario_registro = models.ForeignKey(
        'login.Usuario', on_delete=models.DO_NOTHING,
        db_column='usuario_registro', related_name='contratos_registrados'
    )

    ultima_actualizacion = models.DateTimeField(
        auto_now=True, db_column='ultima_actualizacion')

    class Meta:
        managed = True
        db_table = 'contrato'

    def __str__(self):
        return f"Contrato {self.numero_contrato}"


class ModificacionContratacion(models.Model):  # Nuevo modelo ajustado al SQL
    id = models.AutoField(primary_key=True, db_column='id')
    contrato = models.ForeignKey(
        'Contrato',
        on_delete=models.CASCADE,
        db_column='contrato_id',
        related_name='modificaciones'
    )

    # Suspensiones
    fecha_inicio_suspension = models.DateField(
        null=True, blank=True, db_column='fecha_inicio_suspension')
    fecha_final_suspension = models.DateField(
        null=True, blank=True, db_column='fecha_final_suspension')
    plazo_suspension = models.IntegerField(
        null=True, blank=True, db_column='plazo_suspension')
    unidad_plazo = models.CharField(
        max_length=50, null=True, blank=True, db_column='unidad_plazo')

    fecha_inicio_suspension2 = models.DateField(
        null=True, blank=True, db_column='fecha_inicio_suspension2')
    fecha_final_suspension2 = models.DateField(
        null=True, blank=True, db_column='fecha_final_suspension2')
    plazo_suspension2 = models.IntegerField(
        null=True, blank=True, db_column='plazo_suspension2')
    unidad_plazo2 = models.CharField(
        max_length=50, null=True, blank=True, db_column='unidad_plazo2')

    # Cesión
    cedente = models.CharField(
        max_length=255, null=True, blank=True, db_column='cedente')
    cesionario = models.CharField(
        max_length=255, null=True, blank=True, db_column='cesionario')
    direccion_cedente = models.CharField(
        max_length=255, null=True, blank=True, db_column='direccion_cedente')
    telefono_cedente = models.CharField(
        max_length=50, null=True, blank=True, db_column='telefono_cedente')
    correo_cedente = models.EmailField(
        null=True, blank=True, db_column='correo_cedente')
    identificacion_cedente = models.CharField(
        max_length=100, null=True, blank=True, db_column='identificacion_cedente')
    fecha_modificacion_cesion = models.DateField(
        null=True, blank=True, db_column='fecha_modificacion_cesion')
    fecha_inicio_cesion = models.DateField(
        null=True, blank=True, db_column='fecha_inicio_cesion')

    # Adiciones
    sipse_adicion = models.CharField(
        max_length=255, null=True, blank=True, db_column='sipse_adicion')
    fecha_terminacion_adicion = models.DateField(
        null=True, blank=True, db_column='fecha_terminacion_adicion')
    tiempo_adicion = models.IntegerField(
        null=True, blank=True, db_column='tiempo_adicion')
    valor_adicion = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True, db_column='valor_adicion')
    fecha_adicion = models.DateField(
        null=True, blank=True, db_column='fecha_adicion')
    rp_adicion = models.CharField(
        max_length=255, null=True, blank=True, db_column='rp_adicion')
    fecha_rp_adicion = models.DateField(
        null=True, blank=True, db_column='fecha_rp_adicion')

    sipse_adicion_2 = models.CharField(
        max_length=255, null=True, blank=True, db_column='sipse_adicion_2')
    fecha_terminacion_adicion_2 = models.DateField(
        null=True, blank=True, db_column='fecha_terminacion_adicion_2')
    tiempo_adicion_2 = models.IntegerField(
        null=True, blank=True, db_column='tiempo_adicion_2')
    valor_adicion_2 = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True, db_column='valor_adicion_2')
    fecha_adicion_2 = models.DateField(
        null=True, blank=True, db_column='fecha_adicion_2')
    rp_adicion_2 = models.CharField(
        max_length=255, null=True, blank=True, db_column='rp_adicion_2')
    fecha_rp_adicion_2 = models.DateField(
        null=True, blank=True, db_column='fecha_rp_adicion_2')

    # Prórrogas
    fecha_prorroga = models.DateField(
        null=True, blank=True, db_column='fecha_prorroga')
    plazo_prorroga = models.IntegerField(
        null=True, blank=True, db_column='plazo_prorroga')
    nueva_fecha_terminacion = models.DateField(
        null=True, blank=True, db_column='nueva_fecha_terminacion')

    fecha_prorroga_2 = models.DateField(
        null=True, blank=True, db_column='fecha_prorroga_2')
    plazo_prorroga_2 = models.IntegerField(
        null=True, blank=True, db_column='plazo_prorroga_2')
    nueva_fecha_terminacion_2 = models.DateField(
        null=True, blank=True, db_column='nueva_fecha_terminacion_2')

    fecha_prorroga_3 = models.DateField(
        null=True, blank=True, db_column='fecha_prorroga_3')
    plazo_prorroga_3 = models.IntegerField(
        null=True, blank=True, db_column='plazo_prorroga_3')
    nueva_fecha_terminacion_3 = models.DateField(
        null=True, blank=True, db_column='nueva_fecha_terminacion_3')

    # Revisión contractual y registro
    revision_contractual = models.TextField(
        null=True, blank=True, db_column='revision_contractual')
    crp = models.CharField(max_length=255, null=True,
                           blank=True, db_column='crp')
    fecha_registro = models.DateTimeField(
        auto_now_add=True, db_column='fecha_registro')

    class Meta:
        managed = True
        db_table = 'modificacion_contratacion'

    def __str__(self):
        return f"Modificación {self.id} del contrato {self.contrato_id}"


# Aquí agregamos la función obtener_persona() para que puedas usarla en el formulario.
# class DocumentosContrato(models.Model):
 #   contratista = models.ForeignKey(
  #      'login.Persona',
   #     on_delete=models.CASCADE,
   #     related_name='documentos_contrato',
   #     db_column='contratista_id'
   # )
   # contrato = models.ForeignKey(
   #     'Contrato',
   #     on_delete=models.CASCADE,
   #     null=True,
   #     blank=True,
   #     related_name='documentos',
   #     db_column='contrato_id'
   # )
   # tipo_documento = models.CharField(
   #     max_length=100, db_column='tipo_documento')
   # archivo = models.FileField(
   #     upload_to="contratos/documentos/", db_column='archivo')
   # estado = models.CharField(
   #     max_length=20, default="Pendiente", db_column='estado')
   # fecha_subida = models.DateTimeField(
   #     auto_now_add=True, db_column='fecha_subida')
   # ultima_actualizacion = models.DateTimeField(
   #     auto_now=True, db_column='ultima_actualizacion')

    # class Meta:
    #    managed = True
    #    db_table = 'documentos_contrato'

    # def __str__(self):
    #    return f"{self.tipo_documento} - {self.contratista.primer_nombre} {self.contratista.apellido_paterno}"


# class SeguimientoContrato(models.Model):
#    contrato = models.ForeignKey(
#        'Contrato',
#        on_delete=models.CASCADE,
#        related_name='seguimientos',
#        db_column='contrato_id'
#    )
#    comentario = models.TextField(db_column='comentario')
#    fecha_registro = models.DateTimeField(
#        auto_now_add=True, db_column='fecha_registro')

#    class Meta:
#        managed = True
#        db_table = 'seguimiento_contrato'

#    def __str__(self):
#        return f"Seguimiento {self.contrato.codigo_contrato} - {self.fecha_registro}"


class Funcionario(models.Model):  # COMPLETO
    id = models.OneToOneField(
        'login.Persona',
        on_delete=models.CASCADE,
        db_column='id',
        primary_key=True,
        related_name='funcionario'
    )

    cargo = models.CharField(
        max_length=255, db_column='cargo', default='Sin cargo')
    tipo_contrato = models.CharField(
        max_length=255, db_column='tipo_contrato', default='Prestación de servicios')
    cps = models.CharField(max_length=255, db_column='cps', default='CPS0001')

    area = models.ForeignKey(
        'Area',
        on_delete=models.PROTECT,
        db_column='area_id',
        related_name='funcionarios',
        default=1  # ← debe existir un registro con ID=1 en Area
    )

    subgrupo = models.ForeignKey(
        'Subgrupo',
        on_delete=models.PROTECT,
        db_column='subgrupo_id',
        related_name='funcionarios',
        default=1  # ← debe existir un registro con ID=1 en Subgrupo
    )

    class Meta:
        managed = True
        db_table = 'funcionario'

    def __str__(self):
        return f"Funcionario: {self.id} - {self.cargo}"


class Subgrupo(models.Model):  # COMPLETO
    id = models.AutoField(primary_key=True, db_column='id')
    nombre = models.CharField(
        max_length=255, db_column='nombre', default='Subgrupo X')

    area = models.ForeignKey(
        'Area',
        on_delete=models.PROTECT,
        db_column='area_id',
        related_name='subgrupos',
        default=1  # ← debe existir un registro con ID=1 en Area
    )

    class Meta:
        managed = True
        db_table = 'subgrupo'

    def __str__(self):
        return self.nombre


class Area(models.Model):  # COMPLETO
    id = models.AutoField(primary_key=True, db_column='id')
    nombre = models.CharField(
        max_length=255, db_column='nombre', default='Área General')

    class Meta:
        managed = True
        db_table = 'area'

    def __str__(self):
        return self.nombre
