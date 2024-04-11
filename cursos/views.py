from django.shortcuts import render
from .models import Curso, Inscripcion, Estudiante
from datetime import date
from .forms.curso_form import CursoForm
from django.shortcuts import redirect
import random


def curso_list(request):
    cursos = Curso.objects.select_related("categoria").filter(estado="publicado")
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
            "imagen": curso.imagen.url,
        }
        cursos_data.append(curso_data)
    template = "cursos/curso_list.html"
    context = {"cursos": cursos_data}
    return render(request, template_name=template, context=context)


def curso_list_archive(request):
    cursos = Curso.objects.select_related("categoria").filter(estado="archivado")
    cursos_data = []
    for curso in cursos:
        curso_data = {
            "id": curso.id,
            "nombre": curso.nombre,
            "descripcion": curso.descripcion,
            "categoria": curso.categoria.nombre,
            "imagen": curso.imagen.url,
        }
        cursos_data.append(curso_data)

    context = {"cursos": cursos_data}
    return render(request, "cursos/curso_list_archive.html", context=context)


def curso_detail(request, curso_id):
    curso = (
        Curso.objects.prefetch_related("estudiantes")
        .prefetch_related("instructor")
        .get(id=curso_id)
    )

    imagen_instructor = None
    if curso.instructor is not None:
        imagen_instructor = curso.instructor.avatar.url

    curso_data = {
        "id": curso.id,
        "nombre": curso.nombre,
        "descripcion": curso.descripcion,
        "contenido": curso.contenido,
        "precio": curso.precio,
        "fecha_publicacion": curso.fecha_publicacion,
        "categoria": curso.categoria.nombre,
        "duracion": curso.duracion,
        "num_estudiantes": curso.estudiantes.count(),
        "imagen": curso.imagen.url,
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
            "imagen": curso.imagen.url,
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


def curso_create(request):
    if request.method == "POST":
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("curso_list")
    else:
        form = CursoForm()

    context = {"titulo": "Nuevo Curso", "form": form, "submit": "Crear Curso"}
    # Cambiar plantilla a curso_form_bs.html para ver la versión personalizada de Bootstrap
    return render(request, "cursos/curso_form_bs.html", context)


def curso_update(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    if request.method == "POST":
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            return redirect("curso_list")
    else:
        form = CursoForm(instance=curso)

    context = {"titulo": "Editar Curso", "form": form, "submit": "Actualizar Curso"}
    # Cambiar plantilla a curso_form_bs.html para ver la versión personalizada de Bootstrap
    return render(request, "cursos/curso_form.html", context)


def curso_delete(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    curso.delete()
    return redirect("curso_list")


def curso_archive(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    curso.estado = "archivado"
    curso.save()
    return redirect("curso_list")


def curso_restore(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    curso.estado = "publicado"
    curso.save()
    return redirect("curso_list_archive")


def inscribir_alumno(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    estudiantes_disponibles = Estudiante.objects.exclude(inscripcion__curso=curso)
    if estudiantes_disponibles.count() == 0:
        print("No hay alumnos que no cursen este curso")
        return redirect("curso_detail", curso_id=curso_id)
    alumno_a_inscribir = random.choice(estudiantes_disponibles)
    inscripcion = Inscripcion(estudiante=alumno_a_inscribir, curso=curso)
    inscripcion.save()
    return redirect("curso_detail", curso_id=curso_id)
