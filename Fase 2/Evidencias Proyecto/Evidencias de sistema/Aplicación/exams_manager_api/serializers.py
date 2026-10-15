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

    class Meta:
        model = Paciente
        fields = ['rut', 'nombres', 'apellidos', 'correo', 'celular', 'direccion_id', 'password']

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
    username_field = 'rut'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reemplazamos el campo 'username' por 'rut'
        self.fields['rut'] = serializers.CharField(write_only=True)
        del self.fields[self.username_field]

    def validate(self, attrs):
        rut = attrs.get('rut')
        password = attrs.get('password')

        # Intentamos autenticar usando el RUT como username
        user = authenticate(username=rut, password=password)

        if not user:
            raise AuthenticationFailed('RUT o contraseña incorrectos.')

        if not user.is_active:
            raise AuthenticationFailed('Usuario inactivo.')

        # Generar tokens base
        data = super().validate({'username': user.username, 'password': password})

        # Identificar el rol/tipo de usuario para el frontend
        data['user_type'] = 'unknown'
        if hasattr(user, 'paciente_profile'):
            data['user_type'] = 'paciente'
            data['nombre_completo'] = f"{user.paciente_profile.nombres} {user.paciente_profile.apellidos}"
        elif hasattr(user, 'clinico_profile'):
            data['user_type'] = 'clinico'
            data['nombre_completo'] = f"{user.clinico_profile.nombres} {user.clinico_profile.apellidos}"

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

class ClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinica
        fields = '__all__'

class ClinicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinico
        fields = '__all__'

class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = '__all__'