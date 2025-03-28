from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('cuentas_cobro/', include('cuentas_cobro.urls')),
    path('contratacion/', include('contratacion.urls')),

]

# Permitir acceso a archivos multimedia en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
