
from pathlib import Path

from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Documento


# Página base (el acceso definido aquí es solo para pruebas)
def base(request):
    return render(request, "base.html")


# Página de Login
def login(request):
    return render(request, "exams_manager/login.html")


# Página de Registro
def sign_up(request):
    return render(request, "exams_manager/sign_up.html")


# Página de Subida de Exámenes Médicos
@require_http_methods(["GET", "POST"])
def upload(request):
    MAX_SIZE = 10 * 1024 * 1024  # 10 MB

    EXTENSIONES_PERMITIDAS = {
        ".pdf",
        ".doc",
        ".docx",
        ".jpg",
        ".jpeg",
        ".png",
    }

    if request.method == "POST":
        archivos = request.FILES.getlist("documentos")

        if not archivos:
            messages.error(
                request,
                "Selecciona al menos un archivo."
            )
        else:
            guardados = 0

            for archivo in archivos:
                extension = Path(archivo.name).suffix.lower()

                # Validar extensión
                if extension not in EXTENSIONES_PERMITIDAS:
                    messages.error(
                        request,
                        f'"{archivo.name}" tiene un formato no permitido.'
                    )
                    continue

                # Validar tamaño máximo de 10 MB
                if archivo.size > MAX_SIZE:
                    messages.error(
                        request,
                        f'"{archivo.name}" supera el límite de 10 MB.'
                    )
                    continue

                # Guardar el documento en la base de datos
                Documento.objects.create(
                    archivo=archivo,
                    nombre_original=Path(archivo.name).name,
                    tipo=extension.lstrip(".").upper(),
                    estado="pendiente",
                )

                guardados += 1

            # Mostrar resultado de la carga
            if guardados:
                messages.success(
                    request,
                    f"Se cargaron correctamente {guardados} archivo(s)."
                )

    # Obtener los últimos 10 documentos cargados
    documentos = Documento.objects.all()[:10]

    return render(
        request,
        "exams_manager/upload.html",
        {"documentos": documentos},
    )


# Página de Consulta y Visualización de Exámenes Médicos
def home(request):
    return render(request, "exams_manager/home.html")


# Página del profesional clínico
def clinico(request):
    documentos = [
        {
            "paciente": "Juan Perez",
            "rut": "11.111.111-1",
            "tipo": "Receta Medica",
            "fecha": "01-01-2026",
            "estado": "Disponible",
        },
        {
            "paciente": "Juan Perez",
            "rut": "11.111.111-1",
            "tipo": "Licencia Medica",
            "fecha": "01-01-2026",
            "estado": "Disponible",
        },
        {
            "paciente": "Juan Perez",
            "rut": "11.111.111-1",
            "tipo": "Receta Medica",
            "fecha": "01-01-2026",
            "estado": "Disponible",
        },
    ]

    return render(
        request,
        "exams_manager/clinico.html",
        {"documentos": documentos},
    )


# Página del paciente
def paciente(request):
    documentos = [
        {
            "nombre": "recetamedica.pdf",
            "tipo": "Receta Medica",
            "fecha": "01-01-2025",
            "estado": "Vigente",
        },
        {
            "nombre": "licenciamedica.docx",
            "tipo": "Licencia Medica",
            "fecha": "01-01-2025",
            "estado": "En Revisión",
        },
        {
            "nombre": "licenciamedica.docx",
            "tipo": "Imagenologia",
            "fecha": "01-01-2025",
            "estado": "Vigente",
        },
        {
            "nombre": "recetamedica.pdf",
            "tipo": "Receta Medica",
            "fecha": "01-01-2025",
            "estado": "En Revisión",
        },
        {
            "nombre": "recetamedica.pdf",
            "tipo": "Receta Medica",
            "fecha": "01-01-2025",
            "estado": "Vigente",
        },
        {
            "nombre": "licenciamedica.docx",
            "tipo": "Licencia Medica",
            "fecha": "01-01-2025",
            "estado": "Vigente",
        },
        {
            "nombre": "recetamedica.pdf",
            "tipo": "Receta Medica",
            "fecha": "01-01-2025",
            "estado": "Vigente",
        },
        {
            "nombre": "licenciamedica.docx",
            "tipo": "Licencia Medica",
            "fecha": "01-01-2025",
            "estado": "Expirada",
        },
    ]

    return render(
        request,
        "exams_manager/paciente.html",
        {"documentos": documentos},
    )
