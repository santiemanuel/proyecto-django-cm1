# Generated by Django 5.0.3 on 2024-04-11 21:40

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cursos", "0007_curso_imagen_estudiante_avatar_instructor_avatar_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="curso",
            name="contenido",
            field=tinymce.models.HTMLField(default=""),
        ),
    ]