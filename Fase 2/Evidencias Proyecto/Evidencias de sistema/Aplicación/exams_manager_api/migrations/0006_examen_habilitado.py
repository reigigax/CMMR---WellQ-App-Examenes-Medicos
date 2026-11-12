from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams_manager_api', '0005_alter_paciente_clinica'),
    ]

    operations = [
        migrations.AddField(
            model_name='examen',
            name='habilitado',
            field=models.BooleanField(default=True),
        ),
    ]
