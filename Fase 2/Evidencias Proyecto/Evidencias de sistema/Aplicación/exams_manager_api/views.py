from django.db.models import Q
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import (
    Region, Comuna, Direccion,
    Paciente,
    Clinica,
    Clinico,
    Examen,
)

from .serializers import (
    RegionSerializer, ComunaSerializer, DireccionSerializer,
    PacienteSerializer, ClinicaSerializer, ClinicoSerializer, ExamenSerializer,
    RutTokenObtainPairSerializer, PacienteRegistroSerializer, PacienteResumenSerializer,
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
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        """
        Restringe los exámenes según quién consulta (aplica a listar, ver,
        editar y eliminar):
          - Paciente: solo sus propios exámenes habilitados (los deshabilitados
            por un clínico no le aparecen).
          - Clínico: los exámenes de los pacientes de su clínica y los subidos
            por clínicos de su misma clínica.
          - Cualquier otro usuario: ninguno.
        """
        user = self.request.user
        base = Examen.objects.select_related('paciente', 'clinico').order_by('-fecha_subido', '-id')

        paciente = getattr(user, 'paciente_profile', None)
        if paciente:
            return base.filter(paciente=paciente, habilitado=True)

        clinico = getattr(user, 'clinico_profile', None)
        if clinico:
            return base.filter(
                Q(paciente__clinica_id=clinico.clinica_id) |
                Q(clinico__clinica_id=clinico.clinica_id)
            )

        return base.none()

    def destroy(self, request, *args, **kwargs):
        """
        Los exámenes no se eliminan: DELETE solo los deshabilita (el registro y
        el archivo se conservan, pero el archivo ya no se puede visualizar).
        """
        return self.deshabilitar(request, *args, **kwargs)

    def _cambiar_estado(self, request, habilitado):
        if not hasattr(request.user, 'clinico_profile'):
            return Response(
                {"detail": "Solo un clínico puede cambiar el estado de un documento."},
                status=status.HTTP_403_FORBIDDEN
            )
        examen = self.get_object()  # 404 si el examen no es de su clínica
        examen.habilitado = habilitado
        examen.save(update_fields=['habilitado'])
        return Response(self.get_serializer(examen).data)

    @action(detail=True, methods=['post'])
    def deshabilitar(self, request, pk=None):
        return self._cambiar_estado(request, habilitado=False)

    @action(detail=True, methods=['post'])
    def habilitar(self, request, pk=None):
        return self._cambiar_estado(request, habilitado=True)

    @action(detail=False, methods=['get'], url_path='pacientes-asignables')
    def pacientes_asignables(self, request):
        """Pacientes de la clínica del clínico, a los que puede asignar un documento."""
        clinico = getattr(request.user, 'clinico_profile', None)
        if not clinico:
            return Response(
                {"detail": "Solo un clínico puede asignar documentos a pacientes."},
                status=status.HTTP_403_FORBIDDEN
            )
        pacientes = Paciente.objects.filter(clinica_id=clinico.clinica_id).order_by('nombres', 'apellidos')
        return Response(PacienteResumenSerializer(pacientes, many=True).data)

    def _paciente_asignado_por_clinico(self, serializer, clinico):
        """
        Paciente al que el clínico asigna el documento. Es opcional, pero si se
        indica debe pertenecer a la misma clínica del clínico.
        """
        paciente = serializer.validated_data.get('paciente')
        if paciente and paciente.clinica_id != clinico.clinica_id:
            raise ValidationError({"paciente": "El paciente no pertenece a su clínica."})
        return paciente

    def perform_create(self, serializer):
        user = self.request.user
        paciente = getattr(user, 'paciente_profile', None)
        clinico = getattr(user, 'clinico_profile', None)

        if paciente:
            # Un paciente solo sube documentos para sí mismo (se ignora lo que envíe)
            serializer.save(paciente=paciente, clinico=None)
        elif clinico:
            serializer.save(
                paciente=self._paciente_asignado_por_clinico(serializer, clinico),
                clinico=clinico
            )
        else:
            raise PermissionDenied("Solo pacientes y clínicos pueden subir documentos.")

    def perform_update(self, serializer):
        examen = serializer.instance
        clinico = getattr(self.request.user, 'clinico_profile', None)

        if clinico:
            # El clínico puede reasignar el documento, siempre dentro de su clínica
            paciente = (
                self._paciente_asignado_por_clinico(serializer, clinico)
                if 'paciente' in serializer.validated_data else examen.paciente
            )
            serializer.save(paciente=paciente, clinico=examen.clinico)
        else:
            # Un paciente no puede cambiar a quién pertenece el documento
            serializer.save(paciente=examen.paciente, clinico=examen.clinico)


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