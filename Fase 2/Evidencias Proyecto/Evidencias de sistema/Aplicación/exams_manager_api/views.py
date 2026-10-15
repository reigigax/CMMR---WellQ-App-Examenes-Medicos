from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Region, Comuna, Direccion, Paciente, Clinica, Clinico, Examen
from .serializers import (
    RegionSerializer, ComunaSerializer, DireccionSerializer,
    PacienteSerializer, ClinicaSerializer, ClinicoSerializer, ExamenSerializer,
    RutTokenObtainPairSerializer, PacienteRegistroSerializer
)

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer

class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class ClinicaViewSet(viewsets.ModelViewSet):
    queryset = Clinica.objects.all()
    serializer_class = ClinicaSerializer

class ClinicoViewSet(viewsets.ModelViewSet):
    queryset = Clinico.objects.all()
    serializer_class = ClinicoSerializer

class ExamenViewSet(viewsets.ModelViewSet):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = RutTokenObtainPairSerializer


class RegisterPacienteAPIView(APIView):
    permission_classes = [AllowAny]  # Permite el registro público (sin JWT)

    def post(self, request):
        serializer = PacienteRegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"mensaje": "Paciente registrado con éxito."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)