# Generated by Django 5.0.3 on 2024-04-11 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cursos", "0008_curso_contenido"),
    ]

    operations = [
        migrations.AlterField(
            model_name="curso",
            name="descripcion",
            field=models.CharField(max_length=50),
        ),
    ]
