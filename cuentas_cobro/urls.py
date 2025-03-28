from django.urls import path
from . import views

app_name = 'cuentas_cobro'

urlpatterns = [
    path('', views.lista_cuentas, name='lista_cuentas'),
    # agregado para vista de dashboard con cuenta de cobro JC
    path('listado/', views.lista_cuentas, name='listado_cuentas_cobro'),
    path('crear/', views.crear_cuenta, name='crear_cuenta'),
    path('editar/<int:id>/', views.editar_cuenta, name='editar_cuenta'),
    path('eliminar/<int:id>/', views.eliminar_cuenta, name='eliminar_cuenta'),
]
