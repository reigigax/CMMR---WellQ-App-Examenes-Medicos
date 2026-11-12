# Imagen de la aplicación Django WellQ (front 'exams_manager' + API 'exams_manager_api')
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Instalar dependencias primero para aprovechar la caché de capas de Docker
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar el código del proyecto
COPY . .

EXPOSE 8000

# Aplica migraciones (incluye la carga de init.sql), crea los usuarios de prueba
# y levanta el servidor accesible desde fuera del contenedor.
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py poblar_db && python manage.py runserver 0.0.0.0:8000"]
