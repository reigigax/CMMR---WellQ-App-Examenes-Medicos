from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Urls de Administracion
    path('admin/', admin.site.urls),

    # Urls de la API
    path('api/v1/', include('exams_manager_api.urls')),

    # Urls del frontend
    path('', include('exams_manager.urls')),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
