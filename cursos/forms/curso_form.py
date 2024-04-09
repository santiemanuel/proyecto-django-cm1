from django.forms import ModelForm
from ..models import Curso
from django import forms


class CursoForm(ModelForm):
    class Meta:
        model = Curso
        fields = [
            "nombre",
            "descripcion",
            "precio",
            "fecha_publicacion",
            "instructor",
            "categoria",
            "duracion",
            "destacado",
            "estado",
        ]
        labels = {
            "nombre": "Nombre del curso",
            "descripcion": "Descripción",
            "precio": "Precio",
            "fecha_publicacion": "Fecha de publicación",
            "instructor": "Instructor",
            "categoria": "Categoría",
            "duracion": "Duración",
            "destacado": "Destacado",
            "estado": "Estado",
        }
        help_texts = {
            "duracion": "La duración de la clase está definida en horas/minutos/segundos",
        }
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese nombre del curso",
                    "class": "form-control",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Ingrese la descripción",
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "precio": forms.NumberInput(
                attrs={
                    "placeholder": "Ingrese el precio",
                    "class": "form-control form-control-sm",
                }
            ),
            "fecha_publicacion": forms.DateInput(
                attrs={
                    "type": "date",
                    "placeholder": "Ingrese la fecha",
                    "class": "form-control",
                }
            ),
            "duracion": forms.TimeInput(
                attrs={
                    "placeholder": "Ingrese la duración",
                    "class": "form-control",
                }
            ),
            "instructor": forms.Select(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-control"}),
            "destacado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
