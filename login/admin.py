from django.contrib import admin
from .models import Persona


class PersonaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "primer_nombre", "apellido_paterno",
                    "solicita_permiso_especial", "permiso_aprobado")
    list_filter = ("solicita_permiso_especial", "permiso_aprobado")
    search_fields = ("usuario__username", "primer_nombre", "apellido_paterno")
    actions = ["aprobar_permiso_especial"]

    def aprobar_permiso_especial(self, request, queryset):
        """Aprueba el permiso especial para los usuarios seleccionados."""
        queryset.update(permiso_aprobado=True)
        self.message_user(
            request, "✅ Permiso especial aprobado para los usuarios seleccionados.")

    aprobar_permiso_especial.short_description = "Aprobar permiso especial"


admin.site.register(Persona, PersonaAdmin)
