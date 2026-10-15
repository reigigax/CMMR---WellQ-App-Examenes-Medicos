
from django.db import models


class Documento(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_revision", "En revisión"),
        ("disponible", "Disponible"),
    ]

    archivo = models.FileField(upload_to="documentos/")
    nombre_original = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente",
    )

    def __str__(self):
        return self.nombre_original

    class Meta:
        ordering = ["-fecha_subida"]

