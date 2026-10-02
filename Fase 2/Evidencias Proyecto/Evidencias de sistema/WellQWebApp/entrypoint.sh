#!/bin/sh

# Esperar a que la base de datos PostgreSQL esté lista
echo "Esperando a PostgreSQL en $POSTGRES_HOST:$POSTGRES_PORT..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

echo "PostgreSQL está listo. Aplicando migraciones..."

# Cambiar al directorio donde está el manage.py
cd /app/src

# Aplicar migraciones automáticamente
python manage.py migrate

# Iniciar el servidor de desarrollo en el puerto 0.0.0.0:8000
echo "Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000