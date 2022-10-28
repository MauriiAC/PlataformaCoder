from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView

from .forms import CursoFormulario, ProfesorFormulario
from .models import Curso, Profesor

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


def listaProfesores(request):

    profesores = Profesor.objects.all()

    return render(request, "leerProfesores.html", {"profesores": profesores})


def crea_profesor(request):

    print('method:', request.method)
    print('post: ', request.POST)

    if request.method == 'POST':

        miFormulario = ProfesorFormulario(request.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data

            profesor = Profesor(nombre=data['nombre'], apellido=data['apellido'], email=data['email'], profesion=data['profesion'])
            
            profesor.save()

            return HttpResponseRedirect('/app-coder/')
    
    else:

        miFormulario = ProfesorFormulario()

        return render(request, "profesorFormulario.html", {"miFormulario": miFormulario})

def eliminarProfesor(request, id):

    if request.method == 'POST':

        profesor = Profesor.objects.get(id=id)
        profesor.delete()

        profesores = Profesor.objects.all()

        return render(request, "leerProfesores.html", {"profesores": profesores})        


def editar_profesor(request, id):

    print('method:', request.method)
    print('post: ', request.POST)

    profesor = Profesor.objects.get(id=id)

    if request.method == 'POST':

        miFormulario = ProfesorFormulario(request.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data

            profesor.nombre = data["nombre"]
            profesor.apellido = data["apellido"]
            profesor.email = data["email"]
            profesor.profesion = data["profesion"]

            profesor.save()

            return HttpResponseRedirect('/app-coder/')
    
    else:

        miFormulario = ProfesorFormulario(initial={
            "nombre": profesor.nombre,
            "apellido": profesor.apellido,
            "email": profesor.email,
            "profesion": profesor.profesion,
        })

        return render(request, "editarProfesor.html", {"miFormulario": miFormulario, "id": profesor.id})


class CursoList(ListView):

    model = Curso
    template_name = 'curso_list.html'
    context_object_name = "cursos"

class CursoDetail(DetailView):

    model = Curso
    template_name = 'curso_detail.html'
    context_object_name = "curso"

class CursoCreate(CreateView):

    model = Curso
    template_name = 'curso_create.html'
    fields = ["nombre", "camada"]
    success_url = '/app-coder/'

class CursoUpdate(UpdateView):

    model = Curso
    template_name = 'curso_update.html'
    fields = ('__all__')
    success_url = '/app-coder/'

class CursoDelete(DeleteView):

    model = Curso
    template_name = 'curso_delete.html'
    success_url = '/app-coder/'
