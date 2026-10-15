from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegionViewSet, ComunaViewSet, DireccionViewSet,
    PacienteViewSet, ClinicaViewSet, ClinicoViewSet, ExamenViewSet,
    CustomTokenObtainPairView, RegisterPacienteAPIView, CustomTokenObtainPairView
)

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    
    # Endpoint de registro público
    path('auth/register/paciente/', RegisterPacienteAPIView.as_view(), name='api_register_paciente'),
]

router = DefaultRouter()
router.register(r'regiones', RegionViewSet)
router.register(r'comunas', ComunaViewSet)
router.register(r'direccion', DireccionViewSet)
router.register(r'paciente', PacienteViewSet)
router.register(r'clinica', ClinicaViewSet)
router.register(r'clinico', ClinicoViewSet)
router.register(r'examenes', ExamenViewSet)

urlpatterns += router.urls
