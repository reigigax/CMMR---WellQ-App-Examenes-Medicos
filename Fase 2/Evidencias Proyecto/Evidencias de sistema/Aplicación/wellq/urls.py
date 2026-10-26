from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Urls de Administracion
    path('admin/', admin.site.urls),

    # Urls de la API
    path('api/v1/', include('exams_manager_api.urls')),

    # Urls del frontend
    path('', include('exams_manager.urls')),
]
