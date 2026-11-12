from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.http import Http404
from django.views.static import serve

from exams_manager_api.models import Examen


def servir_media(request, path):
    """
    Sirve los archivos subidos, excepto los de exámenes deshabilitados por un
    clínico: esos devuelven 404 aunque se conozca la URL.
    """
    if Examen.objects.filter(archivo=path, habilitado=False).exists():
        raise Http404("Documento deshabilitado.")
    return serve(request, path, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    # Urls de Administracion
    path('admin/', admin.site.urls),

    # Urls de la API
    path('api/v1/', include('exams_manager_api.urls')),

    # Urls del frontend
    path('', include('exams_manager.urls')),
]
if settings.DEBUG:
    media_prefix = settings.MEDIA_URL.lstrip('/')
    urlpatterns += [
        re_path(rf'^{media_prefix}(?P<path>.*)$', servir_media),
    ]
