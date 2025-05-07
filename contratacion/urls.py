from django.urls import path
from . import views
from .views import eliminar_documento, estado_evaluaciones, asociar_contratista, eliminar_convocatoria,tablero_control

app_name = 'contratacion'

urlpatterns = [
    path('', views.lista_contratos, name='lista_contratos'),
    path('registro-documentacion/', views.registro_documentacion,
         name='registro_documentacion'),
    path("actualizar-datos/", views.actualizar_datos, name="actualizar_datos"),
    path("eliminar-documento/<int:id>/",
         eliminar_documento, name="eliminar_documento"),
    path('listado_hv/', views.listado_Hv, name='listado_Hv'),

    path("convocatorias/asociar/<int:contratista_id>/<int:convocatoria_id>/",
         views.asociar_contratista, name="asociar_contratista"),
    path("convocatorias/asociar/<int:convocatoria_id>/",
         views.seleccionar_contratista, name="seleccionar_contratista"),
    path("convocatorias/eliminar_asociacion/<int:contratista_id>/<int:convocatoria_id>/",
         views.eliminar_asociacion, name="eliminar_asociacion"),


    path('convocatorias/', views.lista_convocatorias, name='lista_convocatorias'),
    path('convocatorias/crear/', views.crear_convocatoria,
         name='crear_convocatoria'),
    path('convocatorias/editar/<int:id>/',
         views.editar_convocatoria, name='editar_convocatoria'),
    path('convocatorias/eliminar/<int:id>/',
         views.eliminar_convocatoria, name='eliminar_convocatoria'),
    path('convocatorias/<int:id>/', views.detalle_convocatoria,
         name='detalle_convocatoria'),

    path('detalle_contratista/<int:id>/', views.detalle_contratista,
         name='detalle_contratista'),  # ✅ Agregamos la URL
    path("evaluar/<int:id>/", views.evaluar_contratista,
         name="evaluar_contratista"),
    path("estado_evaluaciones/", estado_evaluaciones, name="estado_evaluaciones"),
    path('tablero/', tablero_control, name='tablero_control'),

    path('crear/', views.crear_contrato, name='crear_contrato'),
    path('editar/<int:id>/', views.editar_contrato, name='editar_contrato'),
    path('eliminar/<int:id>/', views.eliminar_contrato, name='eliminar_contrato'),






]
