from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls', namespace='login')),
    # path('cuentaCobro/', include('cuentaCobro.urls')),
    # path('certificado/', include('certificado.urls')),
    path('contratacion/', include('contratacion.urls')),
]

# Codigo para visualizar y cargar documentos
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
