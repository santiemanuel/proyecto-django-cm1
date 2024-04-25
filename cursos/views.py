from django.shortcuts import render
from .models import Curso, Inscripcion, Estudiante
from datetime import date
from .forms.curso_form import CursoForm
from .forms.estudiante_form import EstudianteForm
from django.shortcuts import redirect
import random
from .forms.user_form import UserRegisterForm
from .forms.user_form import UserLoginForm
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear estudiante
            Estudiante.objects.create(
                usuario=user, nombre=user.first_name + user.last_name, email=user.email
            )
            login(request, user)
            return redirect(
                "home"
            )  # Redirigir a la página de inicio después del registro
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(
                    "home"
                )  # Redirigir a la página de inicio después del inicio de sesión
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form})


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


def user_logout(request):
    logout(request)
    return redirect("home")


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
        "user": request.user,
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


def estudiante_list(request):
    estudiantes = Estudiante.objects.all()
    context = {"estudiantes": estudiantes}
    template = "estudiante/estudiante_list.html"
    return render(request, template, context)


def estudiante_detail(request, estudiante_id):
    estudiante = Estudiante.objects.get(id=estudiante_id)
    inscripciones = estudiante.inscripcion_set.select_related("curso")

    if request.method == "POST":
        inscripcion_id = request.POST.get("inscripcion_id")
        inscripcion = get_object_or_404(
            Inscripcion, id=inscripcion_id, estudiante=estudiante
        )
        inscripcion.delete()
        return redirect("estudiante_detail", estudiante_id=estudiante.id)

    context = {"estudiante": estudiante, "inscripciones": inscripciones}

    return render(request, "estudiante/estudiante_detail.html", context)


def create_estudiante(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("estudiante_list")
    else:
        form = EstudianteForm()

    context = {"form": form, "submit": "Crear Estudiante", "titulo": "Nuevo Estudiante"}
    return render(request, "estudiante/estudiante_form.html", context)


def update_estudiante(request, usuario_id):
    estudiante = Estudiante.objects.get(usuario=usuario_id)
    if request.method == "POST":
        form = EstudianteForm(request.POST, request.FILES, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect("estudiante_list")
    else:
        form = EstudianteForm(instance=estudiante)

    context = {
        "form": form,
        "submit": "Actualizar Estudiante",
        "titulo": "Editar Estudiante",
    }
    return render(request, "estudiante/estudiante_form.html", context)
