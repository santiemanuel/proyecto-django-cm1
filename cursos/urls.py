"""
URL configuration for proyecto_cursos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path("cursos/", views.curso_list, name="curso_list"),
    path("cursos/archivados/", views.curso_list_archive, name="curso_list_archive"),
    path("cursos/<int:curso_id>/", views.curso_detail, name="curso_detail"),
    path("cursos/crear/", views.curso_create, name="curso_create"),
    path("cursos/<int:curso_id>/editar", views.curso_update, name="curso_update"),
    path("cursos/<int:curso_id>/eliminar", views.curso_delete, name="curso_delete"),
    path("cursos/<int:curso_id>/archivar", views.curso_archive, name="curso_archive"),
    path("cursos/<int:curso_id>/restaurar", views.curso_restore, name="curso_restore"),
    path(
        "cursos/<int:curso_id>/inscribir/",
        views.inscribir_alumno,
        name="inscribir_alumno",
    ),
    path("estudiantes/", views.estudiante_list, name="estudiante_list"),
    path(
        "estudiantes/<int:estudiante_id>/",
        views.estudiante_detail,
        name="estudiante_detail",
    ),
    path("estudiantes/crear/", views.create_estudiante, name="create_estudiante"),
    path(
        "estudiantes/<int:usuario_id>/editar",
        views.update_estudiante,
        name="update_estudiante",
    ),
    path("signup/", views.register, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("", views.home, name="home"),
]
