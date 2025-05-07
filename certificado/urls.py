from django.urls import path
from . import views

app_name = 'certificado'

urlpatterns = [
    
    path('gestionar_funcionario/<uuid:user_id>/', views.gestionar_funcionario, name='gestionar_funcionario'),
    path('generar_certificado/<str:no_identificacion>/', views.generar_certificado, name='generar_certificado'),
    path('preview_certificado/<str:no_identificacion>/', views.preview_certificado, name='preview_certificado'),
    path('listar_cedulas/', views.listar_cedulas, name='listar_cedulas'),
    path('buscar_certificado/', views.buscar_certificado, name='buscar_certificado'),
    path('cargar_csv/', views.cargar_csv, name='cargar_csv'),
    path('descargar_csv/', views.descargar_csv, name='descargar_csv'),
]