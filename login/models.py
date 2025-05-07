from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
import uuid


class Usuario(AbstractUser):  # COMPLETO
    id = models.AutoField(primary_key=True, db_column='id')

    groups = models.ManyToManyField(
        Group, related_name="usuario_groups", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="usuario_permissions", blank=True)

    class Meta:
        managed = True
        db_table = 'usuario'

    def __str__(self):
        return f"{self.username}"


class TipoDocumento(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_documento'

    def __str__(self):
        return self.nombre


class TipoContrato(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_contrato'

    def __str__(self):
        return self.nombre


class Pais(models.Model):  # COMPLETO
    id = models.AutoField(primary_key=True, db_column='id')
    nombre = models.CharField(max_length=100, db_column='nombre')

    class Meta:
        managed = True
        db_table = 'pais'

    def __str__(self):
        return self.nombre


class Departamento(models.Model):  # COMPLETO
    id = models.AutoField(primary_key=True, db_column='id')
    nombre = models.CharField(max_length=255)
    pais = models.ForeignKey(
        'Pais', on_delete=models.PROTECT, db_column='pais_id', related_name='departamentos'
    )

    class Meta:
        managed = True
        db_table = 'departamento'

    def __str__(self):
        return self.nombre


class Municipio(models.Model):  # COMPLETO
    id = models.AutoField(primary_key=True, db_column='id')
    nombre = models.CharField(max_length=255)
    departamento = models.ForeignKey(
        'Departamento', on_delete=models.PROTECT, db_column='departamento_id', related_name='municipios'
    )

    class Meta:
        managed = True
        db_table = 'municipio'

    def __str__(self):
        return self.nombre


class Sexo(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sexo'

    def __str__(self):
        return self.nombre


class IdentidadGenero(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'identidad_genero'

    def __str__(self):
        return self.nombre


class OrientacionSexual(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'orientacion_sexual'

    def __str__(self):
        return self.nombre


class GrupoEtnico(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'grupo_etnico'

    def __str__(self):
        return self.nombre


class TipoDiscapacidad(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_discapacidad'

    def __str__(self):
        return self.nombre


class NivelEducativo(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'nivel_educativo'

    def __str__(self):
        return self.nombre


class Ocupacion(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ocupacion'

    def __str__(self):
        return self.nombre


class SectorEconomico(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sector_economico'

    def __str__(self):
        return self.nombre


class TipoVivienda(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_vivienda'

    def __str__(self):
        return self.nombre


class ServicioBasico(models.Model):  # OK+
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'servicio_basico'

    def __str__(self):
        return self.nombre


class PersonaServicioBasico(models.Model):  # OK +
    persona = models.ForeignKey(
        'Persona', on_delete=models.CASCADE, db_column='persona_id')
    servicio_basico = models.ForeignKey(
        'ServicioBasico', on_delete=models.CASCADE, db_column='servicio_basico_codigo')

    class Meta:
        managed = True
        db_table = 'persona_servicio_basico'
        unique_together = (('persona', 'servicio_basico'),)

    def __str__(self):
        return f"{self.persona} - {self.servicio_basico}"


class TipoDispositivo(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_dispositivo'

    def __str__(self):
        return self.nombre


class PersonaTipoDispositivo(models.Model):  # COMPLETO
    persona = models.ForeignKey(
        'Persona', on_delete=models.CASCADE, db_column='persona_id')
    tipo_dispositivo = models.ForeignKey(
        'TipoDispositivo', on_delete=models.CASCADE, db_column='tipo_dispositivo_codigo')

    class Meta:
        managed = True
        db_table = 'persona_tipo_dispositivo'
        unique_together = (('persona', 'tipo_dispositivo'),)

    def __str__(self):
        return f"{self.persona} - {self.tipo_dispositivo}"


class RedSocial(models.Model):  # COMPLETO
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'red_social'

    def __str__(self):
        return self.nombre


class PersonaRedSocial(models.Model):  # COMPLETO
    persona = models.ForeignKey(
        'Persona', on_delete=models.CASCADE, db_column='persona_id')
    red_social = models.ForeignKey(
        'RedSocial', on_delete=models.CASCADE, db_column='red_social_codigo')

    class Meta:
        managed = True
        db_table = 'persona_red_social'
        unique_together = (('persona', 'red_social'),)

    def __str__(self):
        return f"{self.persona} - {self.red_social}"


class PersonaCuentaBancaria(models.Model):  # COMPLETADO
    id = models.AutoField(primary_key=True, db_column='id')

    persona = models.OneToOneField(
        'Persona',
        on_delete=models.CASCADE,
        db_column='persona_id',
        related_name='cuenta_bancaria'
    )

    banco = models.CharField(max_length=100, db_column='banco')
    tipo_cuenta_bancaria = models.CharField(
        max_length=100, db_column='tipo_cuenta_bancaria')
    numero_cuenta_bancaria = models.CharField(
        max_length=100, db_column='numero_cuenta_bancaria')
    pensionado = models.BooleanField(db_column='pensionado')

    class Meta:
        managed = True
        db_table = 'persona_cuenta_bancaria'

    def __str__(self):
        return f"{self.persona} - {self.numero_cuenta_bancaria}"


class Persona(models.Model):  # COMPLETO
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil")

    ROL_CHOICES = [
        ('contratista', 'Contratista'),
        ('alcaldesa', 'Alcaldesa'),
        ('juridico', 'Jurídico'),
        ('contratacion', 'Contratación'),
        ('financiera', 'Financiera'),
        ('despacho', 'Despacho'),
        ('admin', 'Administrador'),
    ]
    rol = models.CharField(
        max_length=30, choices=ROL_CHOICES, default='contratista', db_column='rol')

    primer_nombre = models.CharField(max_length=50, db_column='nombre1')  # ok
    segundo_nombre = models.CharField(
        max_length=50, blank=True, null=True, db_column='nombre2')  # ok
    apellido_paterno = models.CharField(
        max_length=50, db_column='apellido1')  # ok
    apellido_materno = models.CharField(
        max_length=50, blank=True, null=True, db_column='apellido2')  # ok
    fecha_expedicion = models.DateField(
        null=True, blank=True, db_column='fecha_expedicion')  # ok

    no_identificacion = models.CharField(
        max_length=50, unique=True, db_column='numero_documento')  # ok

    # Relación con catálogos
    tipo_documento = models.ForeignKey(  # ok
        'TipoDocumento', on_delete=models.DO_NOTHING, db_column='tipo_documento', blank=True, null=True)
    lugar_nacimiento = models.ForeignKey('Municipio', on_delete=models.DO_NOTHING,  # ok
                                         db_column='lugar_nacimiento', blank=True, null=True, related_name='personas_lugar_nacimiento')
    sexo_biologico = models.ForeignKey(
        'Sexo', on_delete=models.DO_NOTHING, db_column='sexo_biologico', blank=True, null=True)  # ok
    identidad_genero = models.ForeignKey(  # ok
        'IdentidadGenero', on_delete=models.DO_NOTHING, db_column='identidad_genero', blank=True, null=True)
    orientacion_sexual = models.ForeignKey(  # ok
        'OrientacionSexual', on_delete=models.DO_NOTHING, db_column='orientacion_sexual', blank=True, null=True)
    grupo_etnico = models.ForeignKey(  # ok
        'GrupoEtnico', on_delete=models.DO_NOTHING, db_column='grupo_etnico', blank=True, null=True, related_name='personas_residentes')
    tipo_discapacidad = models.ForeignKey(  # ok
        'TipoDiscapacidad', on_delete=models.DO_NOTHING, db_column='tipo_discapacidad', blank=True, null=True)
    municipio_residencia = models.ForeignKey(  # validar como se une con municipio
        'Municipio', on_delete=models.DO_NOTHING, db_column='municipio_residencia', blank=True, null=True)
    nivel_formacion = models.ForeignKey(
        'NivelEducativo', on_delete=models.DO_NOTHING, db_column='nivel_educativo', blank=True, null=True)  # ok
    profesion = models.ForeignKey(
        'Ocupacion', on_delete=models.DO_NOTHING, db_column='ocupacion_actual', blank=True, null=True)  # ok
    sector_economico = models.ForeignKey(  # ok
        'SectorEconomico', on_delete=models.DO_NOTHING, db_column='sector_economico', blank=True, null=True)

    tipo_contrato = models.ForeignKey(
        'TipoContrato',
        on_delete=models.DO_NOTHING,
        db_column='tipo_contrato',
        blank=True,
        null=True
    )

    tipo_vivienda = models.ForeignKey(  # ok
        'TipoVivienda', on_delete=models.DO_NOTHING, db_column='tipo_vivienda', null=True)

    # Campos faltantes
    telefono = models.CharField(
        max_length=30, db_column='telefono_principal', blank=True, null=True)
    nacionalidad = models.CharField(
        max_length=50, blank=True, null=True)  # Nacionalidad
    pertenencia_lgbti = models.BooleanField(
        default=False)  # Pertenencia a población LGBTIQ+
    discapacidad = models.BooleanField(default=False)  # ¿Tiene discapacidad?
    victima_conflicto = models.BooleanField(
        default=False)  # ¿Es víctima del conflicto armado?
    migrante = models.BooleanField(default=False)  # ¿Es migrante?
    poblacion_rural = models.BooleanField(
        default=False)  # ¿Pertenece a zona rural?
    zona = models.CharField(max_length=10, choices=[(
        # Zona
        'urbana', 'Urbana'), ('rural', 'Rural')], blank=True, null=True)
    estrato_social = models.IntegerField(
        blank=True, null=True)  # Estrato social
    telefono_secundario = models.CharField(
        max_length=30, blank=True, null=True)  # Teléfono secundario
    actualmente_estudia = models.BooleanField(
        default=False)  # ¿Actualmente estudia?
    institucion = models.CharField(
        max_length=255, blank=True, null=True)  # Institución educativa
    ingresos_mensuales = models.CharField(
        max_length=50, blank=True, null=True)  # Ingresos mensuales
    tipo_construccion = models.CharField(max_length=20, choices=[(
        # Tipo de construcción
        'formal', 'Formal'), ('informal', 'Informal')], blank=True, null=True)
    numero_personas_hogar = models.IntegerField(
        blank=True, null=True)  # Número de personas en el hogar
    afiliacion_salud = models.CharField(max_length=50, choices=[(
        # Afiliación a salud
        'EPS', 'EPS'), ('subsidiado', 'Régimen Subsidiado'), ('no_afiliado', 'No afiliado')], blank=True, null=True)
    enfermedades_cronicas = models.CharField(
        max_length=255, blank=True, null=True)  # Enfermedades crónicas
    acceso_servicios_salud = models.CharField(max_length=20, choices=[('bueno', 'Bueno'), (
        # Acceso a servicios de salud
        'regular', 'Regular'), ('malo', 'Malo')], blank=True, null=True)
    acceso_internet = models.BooleanField(
        default=False)  # ¿Tiene acceso a internet?
    direccion = models.CharField(max_length=255)  # falta agregar
    fecha_nacimiento = models.DateField(
        null=True, blank=True, db_column='fecha_nacimiento')  # falta agregar

    servicios_basicos = models.ManyToManyField(  # ok
        'ServicioBasico',
        through='PersonaServicioBasico',
        related_name='personas'
    )

    tipo_dispositivo = models.ManyToManyField(  # ok
        'TipoDispositivo',
        through='PersonaTipoDispositivo',
        related_name='personas'
    )
    redes_sociales_uso = models.ManyToManyField(
        'RedSocial',
        through='PersonaRedSocial',
        related_name='personas'
    )

    class Meta:
        managed = True
        db_table = 'persona'

    def __str__(self):
        return f"{self.primer_nombre} {self.apellido_paterno}"
