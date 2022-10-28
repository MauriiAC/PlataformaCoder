from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import CursoFormulario
from .models import Curso

# Create your views here.

def curso(request, camada, nombre):

    curso = Curso(nombre=nombre, camada=camada)
    curso.save()

    return HttpResponse(f"""
        <p>Curso: {curso.nombre} - Camada: {curso.camada} agregado! </p>
    """)


def lista_curso(request):

    lista = Curso.objects.all()

    return render(request, "lista_cursos.html", {"lista_cursos": lista})


def inicio(request):
    
    return render(request, "inicio.html")

def cursos(request):

    lista = Curso.objects.all() 

    return render(request, "cursos.html", {"lista_cursos": lista})

def profesores(request):
    
    return render(request, "profesores.html")

def estudiantes(request):
    
    return render(request, "estudiantes.html")

def entregables(request):
    
    return render(request, "estudiantes.html")


def cursoFormulario(request):

    print('method:', request.method)
    print('post: ', request.POST)

    if request.method == 'POST':

        miFormulario = CursoFormulario(request.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data

            curso = Curso(nombre=data['curso'], camada=data['camada'])
            curso.save()

            return HttpResponseRedirect('/app-coder/')
    
    else:

        miFormulario = CursoFormulario()

        return render(request, "cursoFormulario.html", {"miFormulario": miFormulario})
        

def busquedaCamada(request):

    return render(request, 'busquedaCamada.html')


def buscar(request):
 

    if request.GET["camada"]:

        camada = request.GET["camada"]

        cursos = Curso.objects.filter(camada__icontains=camada)

        return render(request, "resultadoBusqueda.html", {"cursos": cursos, "camada": camada})

    else:

        respuesta = "No enviaste datos"

    return HttpResponse(respuesta)