from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User



class Region(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    numero = models.CharField(max_length=4)

    class Meta:
        db_table = 'region'

    def __str__(self):
        return self.nombre



class Comuna(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_column='region_fk',
        related_name='comunas'
    )

    class Meta:
        db_table = 'comuna'

    def __str__(self):
        return self.nombre



class Direccion(models.Model):
    id = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=75)
    numero = models.SmallIntegerField(null=True, blank=True)
    
    comuna = models.ForeignKey(
        Comuna,
        on_delete=models.CASCADE,
        db_column='comuna_fk',
        related_name='direcciones'
    )

    class Meta:
        db_table = 'direccion'

    def __str__(self):
        return f"{self.calle} {self.numero or ''}".strip()


class Paciente(models.Model):
    id = models.SmallAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paciente_profile', null=True, blank=True)
    rut = models.CharField(max_length=9, unique=True)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=250)
    correo = models.CharField(max_length=250, unique=True)
    celular = models.BigIntegerField(null=True, blank=True)

    direccion = models.ForeignKey(
        Direccion,
        on_delete=models.CASCADE,
        db_column='direccion_fk',
        related_name='pacientes'
    )

    class Meta:
        db_table = 'paciente'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"



class Clinica(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombre = models.CharField(max_length=75)

    direccion = models.ForeignKey(
        Direccion,
        on_delete=models.CASCADE,
        db_column='direccion_fk',
        related_name='clinicas'
    )

    class Meta:
        db_table = 'clinica'

    def __str__(self):
        return self.nombre


class Clinico(models.Model):
    id = models.SmallAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clinico_profile', null=True, blank=True)
    rut = models.CharField(max_length=9)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    correo = models.CharField(max_length=250, unique=True)
    celular = models.BigIntegerField(null=True, blank=True)

    clinica = models.ForeignKey(
        Clinica,
        on_delete=models.CASCADE,
        db_column='clinica_fk',
        related_name='clinicos'
    )

    direccion = models.ForeignKey(
        Direccion,
        on_delete=models.CASCADE,
        db_column='direccion_fk',
        related_name='clinicos'
    )

    class Meta:
        db_table = 'clinico'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"



class Examen(models.Model):
    id = models.SmallAutoField(primary_key=True)
    titulo = models.CharField(max_length=150)
    sesion = models.CharField(max_length=150)
    nota_clinica = models.CharField(max_length=500, null=True, blank=True)
    fecha_subido = models.DateField(auto_now_add=True)
    version_archivo = models.SmallIntegerField(default=1)

    archivo = models.FileField(
        upload_to='examenes_pdf/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='Solo se permiten archivos en formato PDF'
    )
    
    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        db_column='paciente_fk'
    )
    clinico = models.ForeignKey(
        Clinico, 
        on_delete=models.CASCADE, 
        db_column='clinico_fk'
    )

    class Meta:
        db_table = 'examen'

    def __str__(self):
        return f"{self.titulo} - {self.paciente}"