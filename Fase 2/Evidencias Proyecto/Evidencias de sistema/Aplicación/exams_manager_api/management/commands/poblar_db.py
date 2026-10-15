import os
from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.models import User
from exams_manager_api.models import Clinico, Paciente


class Command(BaseCommand):
    help = 'Ejecuta el archivo init.sql y genera los usuarios con contraseñas en auth_user.'

    def handle(self, *args, **options):
        # 1. Ruta e inserción del SQL base
        sql_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
            'init.sql'
        )

        if not os.path.exists(sql_path):
            self.stdout.write(self.style.ERROR(f"No se encontró el archivo SQL en: {sql_path}"))
            return

        self.stdout.write("Ejecutando script init.sql en la base de datos...")

        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_statements = f.read()

        with connection.cursor() as cursor:
            cursor.execute(sql_statements)

        self.stdout.write(self.style.SUCCESS("✔ Script SQL cargado correctamente."))

        # 2. Generación automática de cuentas auth_user para Clínicos
        self.stdout.write("Generando usuarios y contraseñas para Clínicos...")
        clave_clinico_defecto = "Clinico123!"

        for c in Clinico.objects.filter(user__isnull=True):
            user, created = User.objects.get_or_create(
                username=c.rut,
                defaults={
                    'email': c.correo,
                    'first_name': c.nombres,
                    'last_name': c.apellidos
                }
            )
            user.set_password(clave_clinico_defecto)
            user.save()

            c.user = user
            c.save()

        self.stdout.write(self.style.SUCCESS(
            f"✔ Usuarios de Clínicos creados. Contraseña por defecto: {clave_clinico_defecto}"
        ))

        # 3. Generación automática de cuentas auth_user para Pacientes (si existiesen en init.sql)
        clave_paciente_defecto = "Paciente123!"
        for p in Paciente.objects.filter(user__isnull=True):
            user, created = User.objects.get_or_create(
                username=p.rut,
                defaults={
                    'email': p.correo,
                    'first_name': p.nombres,
                    'last_name': p.apellidos
                }
            )
            user.set_password(clave_paciente_defecto)
            user.save()

            p.user = user
            p.save()

        self.stdout.write(self.style.SUCCESS("¡Proceso de poblamiento finalizado con éxito!"))