import requests
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages

API_BASE_URL = "http://127.0.0.1:8000/api/v1"


# ------------------------------------------------------------------
# Decorador de protección para validar la presencia del token JWT
# ------------------------------------------------------------------
def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        access_token = request.session.get('access_token')
        if not access_token:
            messages.warning(request, "Debes iniciar sesión para acceder a esta sección.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ------------------------------------------------------------------
# Vistas NO protegidas (Públicas / Autenticación)
# ------------------------------------------------------------------

def login(request):
    if request.method == 'POST':
        rut_raw = request.POST.get('rut', '')
        # Elimina puntos y guión para enviar solo los dígitos/k
        rut = rut_raw.replace('.', '').replace('-', '').strip()
        password = request.POST.get('password')

        # Petición a la API...

        # Enviar credenciales a la API
        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/login/",
                json={'rut': rut, 'password': password},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                
                # Guardar los tokens JWT y datos de usuario en la sesión de Django
                request.session['access_token'] = data.get('access')
                request.session['refresh_token'] = data.get('refresh')
                request.session['user_type'] = data.get('user_type')
                request.session['nombre_completo'] = data.get('nombre_completo')

                messages.success(request, f"Bienvenido/a {data.get('nombre_completo')}")
                return redirect('home')
            else:
                error_msg = response.json().get('detail', 'Credenciales inválidas')
                messages.error(request, error_msg)

        except requests.exceptions.RequestException:
            messages.error(request, "Error de conexión con el servidor de autenticación.")

    return render(request, 'exams_manager/login.html')


def logout_view(request):
    request.session.flush()
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')


# ------------------------------------------------------------------
# Vistas Protegidas (Requieren JWT en Sesión)
# ------------------------------------------------------------------
@jwt_required
def base(request):
    return render(request, 'base.html')


def sign_up(request):
    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo', '').strip()
        email = request.POST.get('email', '').strip()
        rut_raw = request.POST.get('rut', '').strip()
        celular = request.POST.get('celular', '').strip()
        password = request.POST.get('password', '')
        direccion_id = request.POST.get('direccion_id', 1)

        # Separar Nombre completo en nombres y apellidos
        partes_nombre = nombre_completo.split(' ', 1)
        nombres = partes_nombre[0]
        apellidos = partes_nombre[1] if len(partes_nombre) > 1 else ' '

        # Limpiar el RUT (remover puntos y guión)
        rut = rut_raw.replace('.', '').replace('-', '').upper()

        payload = {
            'rut': rut,
            'nombres': nombres,
            'apellidos': apellidos,
            'correo': email,
            'celular': int(celular) if celular else None,
            'direccion_id': int(direccion_id),
            'password': password
        }

        try:
            response = requests.post(f"{API_BASE_URL}/auth/register/paciente/", json=payload, timeout=5)

            if response.status_code == 201:
                messages.success(request, "¡Cuenta creada exitosamente! Ya puedes iniciar sesión.")
                return redirect('login')
            else:
                errores = response.json()
                msg = "Error al registrar la cuenta."
                if isinstance(errores, dict):
                    # Formatear el primer mensaje de error devuelto por la API
                    primer_campo = next(iter(errores))
                    msg = f"{primer_campo.capitalize()}: {errores[primer_campo][0] if isinstance(errores[primer_campo], list) else errores[primer_campo]}"
                messages.error(request, msg)

        except requests.exceptions.RequestException:
            messages.error(request, "Error de conexión con el servidor de la API.")

    return render(request, 'exams_manager/sign_up.html')


@jwt_required
def upload(request):
    return render(request, 'exams_manager/upload.html')


@jwt_required
def home(request):
    return render(request, 'exams_manager/home.html')


@jwt_required
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


@jwt_required
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
        {
            "documentos": documentos
        }
    )