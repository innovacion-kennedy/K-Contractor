from django.contrib import admin
from .models import Persona, PersonaCuentaBancaria, PersonaServicioBasico, PersonaTipoDispositivo, PersonaRedSocial
from .models import (
    Usuario, TipoDocumento, Municipio, Sexo, IdentidadGenero, OrientacionSexual,
    GrupoEtnico, TipoDiscapacidad, NivelEducativo, Ocupacion,
    SectorEconomico, TipoVivienda, ServicioBasico, TipoDispositivo, RedSocial
)


class CuentaBancariaInline(admin.StackedInline):
    model = PersonaCuentaBancaria
    extra = 0
    max_num = 1
    can_delete = False
    autocomplete_fields = ['persona']


class ServicioBasicoInline(admin.TabularInline):
    model = PersonaServicioBasico
    extra = 0
    autocomplete_fields = ['servicio_basico']


class TipoDispositivoInline(admin.TabularInline):
    model = PersonaTipoDispositivo
    extra = 0
    autocomplete_fields = ['tipo_dispositivo']


class RedSocialInline(admin.TabularInline):
    model = PersonaRedSocial
    extra = 0
    autocomplete_fields = ['red_social']


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        "usuario", "primer_nombre", "segundo_nombre", "apellido_paterno",
        "apellido_materno", "rol", "telefono", "nivel_formacion", "tipo_vivienda"
    )
    list_filter = (
        "rol", "nivel_formacion", "tipo_vivienda", "sector_economico",
        "municipio_residencia", "sexo_biologico", "grupo_etnico"
    )
    search_fields = (
        "usuario__username", "primer_nombre", "apellido_paterno",
        "no_identificacion", "direccion", "telefono"
    )
    autocomplete_fields = (
        "usuario", "tipo_documento", "lugar_nacimiento", "sexo_biologico",
        "identidad_genero", "orientacion_sexual", "grupo_etnico",
        "tipo_discapacidad", "municipio_residencia", "nivel_formacion",
        "profesion", "sector_economico", "tipo_vivienda"
    )
    inlines = [
        CuentaBancariaInline,
        ServicioBasicoInline,
        TipoDispositivoInline,
        RedSocialInline,
    ]
    ordering = ("apellido_paterno", "primer_nombre")
    list_per_page = 25


# ================== Registros para autocompletables ================== #

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(Sexo)
class SexoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(IdentidadGenero)
class IdentidadGeneroAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(OrientacionSexual)
class OrientacionSexualAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(GrupoEtnico)
class GrupoEtnicoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(TipoDiscapacidad)
class TipoDiscapacidadAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(NivelEducativo)
class NivelEducativoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(Ocupacion)
class OcupacionAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(SectorEconomico)
class SectorEconomicoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(TipoVivienda)
class TipoViviendaAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(ServicioBasico)
class ServicioBasicoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(TipoDispositivo)
class TipoDispositivoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(RedSocial)
class RedSocialAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email', 'first_name', 'last_name']
