import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages

API_BASE_URL = "http://127.0.0.1:8000/api/v1"
ZONA_CHILE = ZoneInfo("America/Santiago")


# ------------------------------------------------------------------
# Excepción y Helper Centralizado para la API
# ------------------------------------------------------------------
class TokenExpiredException(Exception):
    """Excepción lanzada cuando la API responde con HTTP 401 Unauthorized."""
    pass


def api_request(request, method, endpoint, data=None, files=None, json=None, timeout=10):
    """
    Función centralizada para realizar peticiones a la API REST.
    Si la API responde con un estado 401 (Unauthorized), interrumpe el flujo
    lanzando TokenExpiredException.
    """
    access_token = request.session.get('access_token')
    headers = {}
    
    if access_token:
        headers['Authorization'] = f"Bearer {access_token}"

    url = f"{API_BASE_URL}/{endpoint.lstrip('/')}"

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            files=files,
            json=json,
            timeout=timeout
        )

        # Si el token caducó o es inválido en la API, lanzamos la excepción
        if response.status_code == 401:
            raise TokenExpiredException()

        return response
    except requests.exceptions.RequestException:
        return None


# ------------------------------------------------------------------
# Decoradores de Protección con Captura Global de Caducidad
# ------------------------------------------------------------------
def jwt_required(view_func):
    """
    Verifica que exista token en la sesión y captura automáticamente 
    si el token caduca durante cualquier operación.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('access_token'):
            messages.error(request, "Sesion de Usuario ha Caducado")
            return redirect('login')

        try:
            return view_func(request, *args, **kwargs)
        except TokenExpiredException:
            request.session.flush()
            messages.error(request, "Sesion de Usuario ha Caducado")
            return redirect('login')

    return _wrapped_view


def clinico_required(view_func):
    """
    Verifica que la sesión corresponda a un perfil clínico y gestiona
    la caducidad del token de forma global.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('access_token'):
            messages.error(request, "Sesion de usuario ha caducado")
            return redirect('login')

        user_type = request.session.get('user_type')
        if user_type != 'clinico':
            messages.error(request, "Acceso restringido: Esta sección requiere perfil clínico.")
            return redirect('paciente')

        try:
            return view_func(request, *args, **kwargs)
        except TokenExpiredException:
            request.session.flush()
            messages.error(request, "Sesion de usuario ha caducado")
            return redirect('login')

    return _wrapped_view


# ------------------------------------------------------------------
# Vistas Públicas / Autenticación
# ------------------------------------------------------------------
def login(request):
    # Redirección si la sesión aún se encuentra activa
    if request.session.get('access_token'):
        if request.session.get('user_type') == 'clinico':
            return redirect('clinico')
        return redirect('paciente')

    if request.method == 'POST':
        rut_raw = request.POST.get('rut', '')
        rut = rut_raw.replace('.', '').replace('-', '').strip()
        password = request.POST.get('password')

        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/login/",
                json={'rut': rut, 'password': password},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                
                request.session['access_token'] = data.get('access')
                request.session['refresh_token'] = data.get('refresh')
                request.session['user_type'] = data.get('user_type')
                request.session['nombre_completo'] = data.get('nombre_completo')
                request.session['rut'] = rut

                messages.success(request, f"Bienvenido/a {data.get('nombre_completo')}")
                
                if data.get('user_type') == 'clinico':
                    return redirect('clinico')
                return redirect('paciente')
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


def sign_up(request):
    if request.session.get('access_token'):
        return redirect('paciente')

    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo', '').strip()
        email = request.POST.get('email', '').strip()
        rut_raw = request.POST.get('rut', '').strip()
        celular = request.POST.get('celular', '').strip()
        password = request.POST.get('password', '')
        direccion_id = request.POST.get('direccion_id', 1)

        partes_nombre = nombre_completo.split(' ', 1)
        nombres = partes_nombre[0]
        apellidos = partes_nombre[1] if len(partes_nombre) > 1 else ' '
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
                    primer_campo = next(iter(errores))
                    msg = f"{primer_campo.capitalize()}: {errores[primer_campo][0] if isinstance(errores[primer_campo], list) else errores[primer_campo]}"
                messages.error(request, msg)

        except requests.exceptions.RequestException:
            messages.error(request, "Error de conexión con el servidor de la API.")

    return render(request, 'exams_manager/sign_up.html')


# ------------------------------------------------------------------
# Saludo personalizado
# ------------------------------------------------------------------
def saludo_actual(request):
    """
    Devuelve el saludo según la hora de Chile (America/Santiago):
    "Buenos días", "Buenas tardes" o "Buenas noches".
    """
    hora = datetime.now(ZONA_CHILE).hour

    if 6 <= hora < 12:
        return "Buenos días"
    if 12 <= hora < 20:
        return "Buenas tardes"
    return "Buenas noches"


# ------------------------------------------------------------------
# Vistas Protegidas
# ------------------------------------------------------------------
@jwt_required
def upload(request):
    if request.method == 'POST':
        archivos = request.FILES.getlist('documentos')

        if not archivos:
            messages.error(request, "No se seleccionó ningún archivo para subir.")
            return redirect('upload')

        exitos = 0
        errores = 0

        for f in archivos:
            files = {'archivo': (f.name, f.read(), f.content_type)}
            data = {
                'titulo': f.name,
                'sesion': 'Sesión Portal Web',
                'nota_clinica': 'Documento cargado desde el panel de usuario.',
                'version_archivo': 1
            }

            response = api_request(request, 'POST', '/examenes/', data=data, files=files, timeout=15)

            if response and response.status_code in [200, 201]:
                exitos += 1
            else:
                errores += 1

        if exitos > 0:
            messages.success(request, f"Se cargaron {exitos} documento(s) correctamente.")
        if errores > 0:
            messages.error(request, f"Ocurrió un error al procesar {errores} archivo(s).")

        return redirect('upload')

    response = api_request(request, 'GET', '/examenes/')
    documentos = response.json() if (response and response.status_code == 200) else []

    context = {
        "nombre_completo": request.session.get('nombre_completo', 'Usuario'),
        "rut": request.session.get('rut', ''),
        "user_type": request.session.get('user_type'),
        "documentos": documentos
    }

    return render(request, 'exams_manager/upload.html', context)


@clinico_required
def clinico(request):
    response = api_request(request, 'GET', '/examenes/')
    documentos = response.json() if (response and response.status_code == 200) else []

    return render(
        request,
        "exams_manager/clinico.html",
        {
            "nombre_completo": request.session.get('nombre_completo'),
            "rut": request.session.get('rut'),
            "documentos": documentos
        },
    )


@jwt_required
def paciente(request):
    response = api_request(request, 'GET', '/examenes/')
    documentos = response.json() if (response and response.status_code == 200) else []

    context = {
        "nombre_completo": request.session.get('nombre_completo', 'Paciente'),
        "rut": request.session.get('rut', 'Sin RUT registrado'),
        "user_type": request.session.get('user_type'),
        "documentos": documentos,
        "saludo": saludo_actual(request)
    }

    return render(request, "exams_manager/paciente.html", context)

@jwt_required
def eliminar_examen(request, examen_id):
    """Envía una petición DELETE a la API para eliminar un examen por su ID."""
    if request.method == 'POST':
        response = api_request(request, 'DELETE', f'/examenes/{examen_id}/')

        if response and response.status_code in [200, 204]:
            messages.success(request, "El documento ha sido eliminado exitosamente.")
        else:
            messages.error(request, "No se pudo eliminar el documento. Intente nuevamente.")

    # Redirige de vuelta a la página desde donde se solicitó la eliminación
    return redirect(request.META.get('HTTP_REFERER', 'clinico'))