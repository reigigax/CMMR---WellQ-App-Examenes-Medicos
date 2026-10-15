import os
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Ejecuta el archivo init.sql en la base de datos PostgreSQL después de migrar.'

    def handle(self, *args, **options):
        # Ruta hacia el archivo init.sql en la raíz del proyecto
        sql_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'init.sql')

        if not os.path.exists(sql_path):
            self.stdout.write(self.style.ERROR(f"No se encontró el archivo SQL en: {sql_path}"))
            return

        self.stdout.write("Ejecutando script init.sql en la base de datos...")

        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_statements = f.read()

        with connection.cursor() as cursor:
            cursor.execute(sql_statements)

        self.stdout.write(self.style.SUCCESS("¡Script SQL ejecutado e inserciones cargadas exitosamente!"))