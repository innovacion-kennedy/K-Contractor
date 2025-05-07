from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from login.models import Usuario
from .models import Funcionario, Radicado, Cesion


@admin.register(Usuario)  # COMPLETADO
class UsuarioAdmin(UserAdmin):
    list_display = ["id", "username", "email", "first_name", "last_name"]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering = ["username"]


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('primer_nombre', 'no_identificacion',
                    'role', 'CPS', 'sitio_expedicion', 'esta_activo')
    search_fields = ('primer_nombre', 'no_identificacion', 'CPS', 'correo')
    list_filter = ('role', 'sitio_expedicion', 'estado')
    readonly_fields = ('esta_activo',)

    def esta_activo(self, obj):
        return obj.esta_activo()
    esta_activo.boolean = True
    esta_activo.short_description = '¿Está activo?'


@admin.register(Radicado)
class RadicadoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'contrato', 'fecha_radicado', 'año_radicado')
    search_fields = ('numero', 'contrato__codigo_contrato', 'descripcion')
    list_filter = ('fecha_radicado',)

    def año_radicado(self, obj):
        return obj.año_radicado()
    año_radicado.short_description = 'Año de Radicado'


@admin.register(Cesion)
class CesionAdmin(admin.ModelAdmin):
    list_display = ('cedente', 'cesionario', 'fecha_cesion', 'descripcion')
    search_fields = ('cedente', 'cesionario', 'descripcion')
    list_filter = ('fecha_cesion',)
