# Generated by Django 5.0.3 on 2024-03-26 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cursos", "0002_categoria_curso_duracion_curso_estado_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="curso",
            name="destacado",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="curso",
            name="requisitos",
            field=models.TextField(blank=True),
        ),
    ]
