from django.urls import path
from . import views

app_name = 'login'


urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('registro/', views.registro_view, name='registro_view'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard-vista/', views.dashboard_view,
         name='dashboard_vista'),
    path('perfil/', views.perfil, name='perfil'),
    path('completar-perfil/', views.completar_perfil, name='completar_perfil'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
]
