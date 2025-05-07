from django.urls import path
from .views import (
    listado_cuentas_cobro,
    generar_cuenta_cobro,
    ver_cuenta_cobro,
    datos_contrato,
    obtener_obligaciones_por_contrato,
    subir_obligaciones,
    visualizar_obligaciones,  
    generar_pdf,

)
app_name = 'cuentaCobro' 

urlpatterns = [
    path("", listado_cuentas_cobro, name="listado_cuentas_cobro"),
    path("nueva/", generar_cuenta_cobro, name="generar_cuenta_cobro"),
    path("<int:cuenta_id>/", ver_cuenta_cobro, name="ver_cuenta_cobro"),
    path("datos_contrato/<int:contrato_id>/", datos_contrato, name="datos_contrato"),
    path("subir_obligaciones/", subir_obligaciones, name="subir_obligaciones"),
    path("obligaciones_por_contrato/<int:contrato_id>/", obtener_obligaciones_por_contrato, name="obligaciones_por_contrato"),
    path("visualizar_obligaciones/", visualizar_obligaciones, name="visualizar_obligaciones"),  
    path('generar-pdf/', generar_pdf, name='generar_pdf'),
]
