# Imports de librerias
from django.db import transaction
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Imports locales del proyecto
from .models import Region, Comuna, Direccion, Paciente, Clinica, Clinico, Examen


class PacienteRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    direccion_id = serializers.IntegerField(write_only=True, required=False, default=1)
    # Clínica elegida por el paciente en el formulario de registro (obligatoria)
    clinica = serializers.PrimaryKeyRelatedField(
        queryset=Clinica.objects.all(),
        error_messages={
            'required': "Debe seleccionar una clínica.",
            'null': "Debe seleccionar una clínica.",
            'does_not_exist': "La clínica seleccionada no existe.",
            'incorrect_type': "La clínica seleccionada no es válida.",
        },
    )

    class Meta:
        model = Paciente
        fields = ['rut', 'nombres', 'apellidos', 'correo', 'celular', 'direccion_id', 'clinica', 'password']

    def validate_rut(self, value):
        if Paciente.objects.filter(rut=value).exists() or User.objects.filter(username=value).exists():
            raise serializers.ValidationError("El RUT ya se encuentra registrado.")
        return value

    def validate_correo(self, value):
        if Paciente.objects.filter(correo=value).exists() or User.objects.filter(email=value).exists():
            raise serializers.ValidationError("El correo electrónico ya está registrado.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        direccion_id = validated_data.pop('direccion_id', 1)

        # 1. Obtener o crear una dirección por defecto para evitar que falle si la tabla está vacía
        direccion = Direccion.objects.filter(id=direccion_id).first()
        if not direccion:
            # Si no existe la dirección con ID 1, toma la primera disponible o crea una
            direccion = Direccion.objects.first()
            if not direccion:
                raise serializers.ValidationError({
                    "direccion_id": "No existen direcciones registradas en la base de datos para asociar al paciente."
                })

        # 2. Transacción atómica para crear User y Paciente en conjunto
        #    (la clínica elegida viene en validated_data['clinica'])
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['rut'],
                email=validated_data['correo'],
                password=password,
                first_name=validated_data['nombres'],
                last_name=validated_data['apellidos']
            )

            paciente = Paciente.objects.create(
                user=user,
                direccion=direccion,
                **validated_data
            )

        return paciente

class RutTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Declaramos el campo rut explícitamente
    rut = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eliminamos el campo 'username' que genera SimpleJWT por defecto
        if 'username' in self.fields:
            del self.fields['username']

    def validate(self, attrs):
        rut_raw = attrs.get('rut', '')
        password = attrs.get('password')

        # Limpiamos puntos y guión por si el RUT viene formateado desde el frontend
        rut = rut_raw.replace('.', '').replace('-', '').strip()

        # Autenticamos contra auth_user usando el RUT como username
        user = authenticate(username=rut, password=password)

        if not user:
            raise AuthenticationFailed('RUT o contraseña incorrectos.')

        if not user.is_active:
            raise AuthenticationFailed('Usuario inactivo.')

        # Generar los tokens JWT pasando el diccionario esperado por SimpleJWT
        data = super().validate({'username': user.username, 'password': password})

        # Identificar el tipo de usuario y adjuntar datos al response
        data['user_type'] = 'unknown'
        data['clinica'] = None
        perfil = None
        if hasattr(user, 'paciente_profile'):
            data['user_type'] = 'paciente'
            perfil = user.paciente_profile
        elif hasattr(user, 'clinico_profile'):
            data['user_type'] = 'clinico'
            perfil = user.clinico_profile

        if perfil:
            data['nombre_completo'] = f"{perfil.nombres} {perfil.apellidos}"
            # Nombre de la clínica a la que pertenece (se muestra en el navbar del front)
            data['clinica'] = perfil.clinica.nombre if perfil.clinica_id else None

        return data


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'


class PacienteResumenSerializer(serializers.ModelSerializer):
    """Datos básicos del paciente que se muestran junto a cada examen."""
    class Meta:
        model = Paciente
        fields = ['id', 'rut', 'nombres', 'apellidos', 'clinica']

class ClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinica
        fields = '__all__'

class ClinicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinico
        fields = '__all__'

class ExamenSerializer(serializers.ModelSerializer):
    # Usado por la vista del clínico para mostrar nombre y RUT del paciente
    paciente_detail = PacienteResumenSerializer(source='paciente', read_only=True)

    class Meta:
        model = Examen
        fields = '__all__'
        # Solo se cambia con las acciones 'deshabilitar'/'habilitar' del clínico
        read_only_fields = ['habilitado']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Si el examen está deshabilitado no se entrega la URL del archivo
        if not instance.habilitado:
            data['archivo'] = None
        return data