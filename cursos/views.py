from django.shortcuts import render
from .models import Curso, Inscripcion
from datetime import date


def curso_list(request):
    cursos = Curso.objects.select_related("categoria")
    cursos_data = []
    for curso in cursos:
        curso_data = {
            "id": curso.id,
            "nombre": curso.nombre,
            "descripcion": curso.descripcion,
            "precio": curso.precio,
            "fecha_publicacion": curso.fecha_publicacion,
            "categoria": curso.categoria.nombre,
            "duracion": curso.duracion,
            "num_estudiantes": curso.estudiantes.count(),
            "imagen": f"img/{curso.categoria.color}.png",
        }
        cursos_data.append(curso_data)
    template = "cursos/curso_list.html"
    context = {"cursos": cursos_data}
    return render(request, template_name=template, context=context)


def curso_detail(request, curso_id):
    curso = (
        Curso.objects.prefetch_related("estudiantes")
        .prefetch_related("instructor")
        .get(id=curso_id)
    )

    imagen_instructor = None
    if curso.instructor is not None:
        imagen_instructor = f'img/{curso.instructor.nombre.split(" ")[0]}.png'

    curso_data = {
        "id": curso.id,
        "nombre": curso.nombre,
        "descripcion": curso.descripcion,
        "precio": curso.precio,
        "fecha_publicacion": curso.fecha_publicacion,
        "categoria": curso.categoria.nombre,
        "duracion": curso.duracion,
        "num_estudiantes": curso.estudiantes.count(),
        "imagen": f"img/{curso.categoria.color}.png",
        "instructor": curso.instructor,
        "imagen_instructor": imagen_instructor,
    }
    context = {"curso": curso_data}
    template = "cursos/curso_detail.html"
    return render(request, template_name=template, context=context)


def home(request):
    num_cursos = Curso.objects.filter(estado="publicado").count()
    num_estudiantes = Inscripcion.objects.values("estudiante").count()

    proximo_curso = (
        Curso.objects.filter(estado="publicado", fecha_publicacion__gt=date.today())
        .order_by("fecha_publicacion")
        .first()
    )

    cursos_destacados = Curso.objects.filter(estado="publicado", destacado=True)[:3]

    cursos_destacados_data = []
    for curso in cursos_destacados:
        curso_data = {
            "id": curso.id,
            "nombre": curso.nombre,
            "descripcion": curso.descripcion,
            "imagen": f"img/{curso.categoria.color}.png",
        }
        cursos_destacados_data.append(curso_data)

    context = {
        "num_cursos": num_cursos,
        "num_estudiantes": num_estudiantes,
        "proximo_curso": proximo_curso,
        "cursos_destacados": cursos_destacados_data,
    }
    template = "cursos/home.html"
    return render(request, template_name=template, context=context)
