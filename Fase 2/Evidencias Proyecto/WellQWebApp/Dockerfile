# Usar una imagen oficial de Python compatible con Django 6.1
FROM python:3.12-slim

# Evitar que Python escriba archivos .pyc y forzar salida sin búfer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg y herramientas de red
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código del proyecto
COPY . /app/

# Dar permisos de ejecución al script de entrada
RUN chmod +x /app/entrypoint.sh

# Exponer el puerto de desarrollo
EXPOSE 8000

# Script de inicio
ENTRYPOINT ["/app/entrypoint.sh"]