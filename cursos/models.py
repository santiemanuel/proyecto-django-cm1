from django.db import models
from datetime import timedelta
from datetime import datetime
from django.core.exceptions import ValidationError


class Estudiante(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre


class Instructor(models.Model):
    nombre = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre + " - " + self.color


def precio_positivo(value):
    if value <= 0:
        raise ValidationError("El precio debe ser un número positivo.")


def duracion_minima(value):
    if value < timedelta(hours=1):
        raise ValidationError("La duración del curso no puede ser menor a una hora.")


def fecha_publicacion_futura(value):
    if value <= datetime.now().date():
        raise ValidationError(
            "La fecha de publicación no puede ser en el pasado ni el día actual."
        )


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.IntegerField(validators=[precio_positivo])
    fecha_publicacion = models.DateField(validators=[fecha_publicacion_futura])
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    duracion = models.DurationField(
        default=timedelta(days=0), validators=[duracion_minima]
    )
    estado = models.CharField(
        max_length=20,
        choices=[
            ("borrador", "Borrador"),
            ("publicado", "Publicado"),
            ("archivado", "Archivado"),
        ],
    )
    requisitos = models.TextField(blank=True)
    destacado = models.BooleanField(default=False)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.SET_NULL, null=True, blank=True
    )
    estudiantes = models.ManyToManyField(Estudiante, through="Inscripcion")

    def __str__(self):
        return self.nombre + " - " + str(self.fecha_publicacion)


class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("estudiante", "curso")

    def __str__(self):
        return self.estudiante.nombre + " - " + self.curso.nombre
