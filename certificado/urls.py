from django.urls import path
from . import views

app_name = 'certificado'

urlpatterns = [
    path('', views.home, name='home'),
    path('gestionar_funcionario/<uuid:user_id>/',
         views.gestionar_funcionario, name='gestionar_funcionario'),
    path('eliminar_datos/<str:cedula>/',
         views.eliminar_datos, name='eliminar_datos'),
    path('generar_certificado/<str:cedula>/',
         views.generar_certificado, name='generar_certificado'),
    path('preview_certificado/<str:cedula>/',
         views.preview_certificado, name='preview_certificado'),
    path('listar_cedulas/', views.listar_cedulas, name='listar_cedulas'),
    path('buscar_certificado/', views.buscar_certificado,
         name='buscar_certificado'),
    path('cargar_csv/', views.cargar_csv, name='cargar_csv'),
    path('descargar_csv/', views.descargar_csv, name='descargar_csv'),
]
