"""
Hace obligatoria la clínica del paciente. Va separada de la 0004 porque en
PostgreSQL no se puede alterar la tabla en la misma transacción en que se
actualizaron filas con claves foráneas diferidas.
"""
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams_manager_api', '0004_paciente_clinica'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='clinica',
            field=models.ForeignKey(
                db_column='clinica_fk',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='pacientes',
                to='exams_manager_api.clinica',
            ),
        ),
    ]
