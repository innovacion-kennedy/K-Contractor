from django.db import models
from django.apps import apps  # Importación diferida


class CuentaCobro(models.Model):
    contrato = models.ForeignKey(
        "contratacion.Contrato", on_delete=models.CASCADE, verbose_name="Contrato Asociado"
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()

    def __str__(self):
        return f"Cuenta de cobro - {self.contrato.numero}"
