from django.contrib import admin
from .models import DatosBancarios, PreguntasFiscales, ContratoObligacion, CuentaCobro, CuentaCobroObligacion, PagoPlanilla

@admin.register(DatosBancarios)
class DatosBancariosAdmin(admin.ModelAdmin):
    list_display = ('persona', 'entidad_bancaria', 'tipo_cuenta', 'numero_cuenta')
    search_fields = ('persona__primer_nombre', 'persona__apellido_paterno', 'entidad_bancaria', 'numero_cuenta')
    list_filter = ('entidad_bancaria', 'tipo_cuenta')

@admin.register(PreguntasFiscales)
class PreguntasFiscalesAdmin(admin.ModelAdmin):
    list_display = ('persona', 'soy_pensionado', 'declarante_renta', 'responsable_iva')
    search_fields = ('persona__primer_nombre', 'persona__apellido_paterno')
    list_filter = ('soy_pensionado', 'declarante_renta', 'responsable_iva')

@admin.register(ContratoObligacion)
class ContratoObligacionAdmin(admin.ModelAdmin):
    list_display = ('contrato', 'descripcion', 'orden')
    search_fields = ('contrato__codigo_contrato', 'descripcion')
    list_filter = ('contrato',)

@admin.register(CuentaCobro)
class CuentaCobroAdmin(admin.ModelAdmin):
    list_display = ('contrato', 'numero_pago', 'estado', 'fecha_presentacion', 'valor_total')
    search_fields = ('contrato__codigo_contrato', 'numero_pago')
    list_filter = ('estado', 'fecha_presentacion')

@admin.register(CuentaCobroObligacion)
class CuentaCobroObligacionAdmin(admin.ModelAdmin):
    list_display = ('cuenta_cobro', 'obligacion', 'actividad', 'producto', 'metodo_verificacion')
    search_fields = ('cuenta_cobro__numero_pago', 'obligacion__descripcion')
    list_filter = ('cuenta_cobro', 'obligacion')

@admin.register(PagoPlanilla)
class PagoPlanillaAdmin(admin.ModelAdmin):
    list_display = ('cuenta_cobro', 'numero_planilla', 'periodo_cotizado', 'fecha_pago')
    search_fields = ('cuenta_cobro__numero_pago', 'numero_planilla')
    list_filter = ('fecha_pago', 'periodo_cotizado')