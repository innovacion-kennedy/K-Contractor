from django.db import models
from contratacion.models import Contrato
from login.models import Persona 

class DatosBancarios(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name="datos_bancarios")
    entidad_bancaria = models.CharField(max_length=100)
    tipo_cuenta = models.CharField(max_length=20, choices=[('Ahorros', 'Ahorros'), ('Corriente', 'Corriente')])
    numero_cuenta = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "persona_datos_bancarios"

    def __str__(self):
        return f"{self.persona} - {self.entidad_bancaria} ({self.tipo_cuenta})"

class PreguntasFiscales(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name="preguntas_fiscales")
    soy_pensionado = models.BooleanField(default=False)
    devolucion_saldos = models.BooleanField(default=False)
    declarante_renta = models.BooleanField(default=False)
    contrata_trabajadores = models.BooleanField(default=False)
    ingresos_80_mas = models.BooleanField(default=False)
    responsable_iva = models.BooleanField(default=False)
    aportes_afc = models.BooleanField(default=False)
    aportes_voluntarios_pension = models.BooleanField(default=False)
    intereses_vivienda = models.BooleanField(default=False)
    medicina_prepagada = models.BooleanField(default=False)
    dependientes = models.BooleanField(default=False)

    class Meta:
        db_table = "persona_preguntas_fiscales"

    def __str__(self):
        return f"Preguntas Fiscales - {self.persona}"

class ContratoObligacion(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="obligaciones")
    descripcion = models.TextField()
    orden = models.PositiveIntegerField()  # Define el orden de la obligación dentro del contrato

    class Meta:
        db_table = "contrato_obligacion"
        ordering = ['orden']  # Se mostrarán en orden ascendente por defecto

    def __str__(self):
        return f"{self.orden}. {self.descripcion[:50]}..."

class CuentaCobro(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="cuentas_cobro")
    numero_pago = models.IntegerField()  # Número de pago dentro del contrato
    estado = models.CharField(max_length=20, choices=[
        ('supervision', 'Supervisión'),
        ('administrativa', 'Administrativa'),
        ('despacho', 'Despacho'),
        ('secop', 'SECOP'),
        ('pendiente_pago', 'Pendiente de Pago'),
        ('pagada', 'Pagada'),
    ])
    fecha_presentacion = models.DateField(auto_now_add=True)  # Fecha en que se genera la cuenta
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "cuenta_cobro"

    def __str__(self):
        return f"Cuenta Cobro {self.numero_pago} - {self.contrato.codigo_contrato}"

class CuentaCobroObligacion(models.Model):
    cuenta_cobro = models.ForeignKey(CuentaCobro, on_delete=models.CASCADE, related_name="cuenta_obligaciones")
    obligacion = models.ForeignKey(ContratoObligacion, on_delete=models.CASCADE, related_name="obligaciones_cuenta")
    actividad = models.TextField()
    producto = models.TextField()
    metodo_verificacion = models.TextField()

    class Meta:
        db_table = "cuenta_cobro_obligacion"

    def __str__(self):
        return f"Obligación en Cuenta {self.cuenta_cobro.numero_pago} - {self.obligacion.orden}"

class PagoPlanilla(models.Model):
    cuenta_cobro = models.ForeignKey(CuentaCobro, on_delete=models.CASCADE, related_name="planillas")
    numero_planilla = models.CharField(max_length=50)
    periodo_cotizado = models.CharField(max_length=20)
    fecha_pago = models.DateField()

    class Meta:
        db_table = "pago_planilla"

    def __str__(self):
        return f"Pago {self.numero_planilla} - {self.periodo_cotizado}"