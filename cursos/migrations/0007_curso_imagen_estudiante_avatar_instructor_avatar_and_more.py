# Generated by Django 5.0.3 on 2024-04-11 20:30

import cursos.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cursos", "0006_alter_inscripcion_fecha_inscripcion_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="curso",
            name="imagen",
            field=models.ImageField(
                blank=True, default="cursos/fallback.png", upload_to="cursos"
            ),
        ),
        migrations.AddField(
            model_name="estudiante",
            name="avatar",
            field=models.ImageField(
                blank=True, default="estudiantes/fallback.png", upload_to="estudiantes"
            ),
        ),
        migrations.AddField(
            model_name="instructor",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="instructores/fallback.png",
                upload_to="instructores",
            ),
        ),
        migrations.AlterField(
            model_name="curso",
            name="duracion",
            field=models.DurationField(
                default=datetime.timedelta(0),
                validators=[cursos.models.duracion_minima],
            ),
        ),
        migrations.AlterField(
            model_name="curso",
            name="fecha_publicacion",
            field=models.DateField(validators=[cursos.models.fecha_publicacion_futura]),
        ),
    ]
