"""
Migración de datos: carga el contenido de 'init.sql' (Regiones, Comunas,
Direcciones, Clínicas y Clínicos) una vez que Django ya creó las tablas.

Antes, 'init.sql' se montaba en '/docker-entrypoint-initdb.d/' del contenedor
de Postgres, pero ese script se ejecuta al crear el contenedor, ANTES de
'python manage.py migrate', por lo que fallaba con:
    ERROR: relation "public.region" does not exist
y nunca se volvía a ejecutar (Postgres solo corre esos scripts con el volumen vacío).
"""
from pathlib import Path

import sqlparse
from django.conf import settings
from django.db import migrations

SQL_PATH = Path(settings.BASE_DIR) / 'init.sql'


def cargar_datos_iniciales(apps, schema_editor):
    Region = apps.get_model('exams_manager_api', 'Region')

    # Idempotente: si ya hay datos (p.ej. cargados con 'poblar_db'), no se duplican.
    if Region.objects.using(schema_editor.connection.alias).exists():
        return

    if not SQL_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos iniciales: {SQL_PATH}")

    sql = SQL_PATH.read_text(encoding='utf-8-sig')

    # El esquema 'public.' solo existe en PostgreSQL; se quita para que también funcione con SQLite.
    if schema_editor.connection.vendor != 'postgresql':
        sql = sql.replace('public.', '')

    with schema_editor.connection.cursor() as cursor:
        for statement in sqlparse.split(sql):
            statement = sqlparse.format(statement, strip_comments=True).strip().rstrip(';')
            if statement:
                cursor.execute(statement)


def eliminar_datos_iniciales(apps, schema_editor):
    alias = schema_editor.connection.alias
    for modelo in ('Clinico', 'Clinica', 'Direccion', 'Comuna', 'Region'):
        apps.get_model('exams_manager_api', modelo).objects.using(alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('exams_manager_api', '0002_alter_examen_archivo_alter_examen_clinico_and_more'),
    ]

    operations = [
        migrations.RunPython(cargar_datos_iniciales, eliminar_datos_iniciales),
    ]
