"""
Agrega la clínica al paciente y asigna una a los pacientes ya existentes,
repartiéndolos entre las clínicas (la que tenga menos pacientes primero).
La columna se deja NOT NULL en la migración 0005.
"""
import django.db.models.deletion
from django.db import migrations, models


def asignar_clinica_a_existentes(apps, schema_editor):
    alias = schema_editor.connection.alias
    Paciente = apps.get_model('exams_manager_api', 'Paciente')
    Clinica = apps.get_model('exams_manager_api', 'Clinica')

    pendientes = Paciente.objects.using(alias).filter(clinica__isnull=True).order_by('id')
    if not pendientes.exists():
        return

    clinicas = list(Clinica.objects.using(alias).order_by('id'))
    if not clinicas:
        raise RuntimeError(
            "Hay pacientes registrados pero no existen clínicas para asignarles. "
            "Cargue las clínicas (init.sql) antes de migrar."
        )

    carga = {c.id: Paciente.objects.using(alias).filter(clinica=c).count() for c in clinicas}
    for paciente in pendientes:
        clinica = min(clinicas, key=lambda c: (carga[c.id], c.id))
        paciente.clinica = clinica
        paciente.save(update_fields=['clinica'])
        carga[clinica.id] += 1


class Migration(migrations.Migration):

    dependencies = [
        ('exams_manager_api', '0003_cargar_datos_iniciales'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='clinica',
            field=models.ForeignKey(
                db_column='clinica_fk',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='pacientes',
                to='exams_manager_api.clinica',
            ),
        ),
        migrations.RunPython(asignar_clinica_a_existentes, migrations.RunPython.noop),
    ]
