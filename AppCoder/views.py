from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CursoFormulario, ProfesorFormulario, UserEditForm, UserRegisterForm
from .models import Curso, Profesor, Avatar

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
    
    avatar = Avatar.objects.get(user=request.user)
    return render(request, "inicio.html", {"url": avatar.imagen.url})

@login_required
def cursos(request):

    lista = Curso.objects.all() 

    return render(request, "cursos.html", {"lista_cursos": lista})
    
@staff_member_required(login_url="/app-coder/login")
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


class CursoList(LoginRequiredMixin, ListView):

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


def loginView(request):

    print('method:', request.method)
    print('post: ', request.POST)

    if request.method == 'POST':

        miFormulario = AuthenticationForm(request, data=request.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data

            usuario = data["username"]
            psw = data["password"]

            user = authenticate(username=usuario, password=psw)

            if user:

                login(request, user)

                return render(request, "inicio.html", {"mensaje": f'Bienvenido {usuario}'})
            
            else:

                return render(request, "inicio.html", {"mensaje": f'Error, datos incorrectos'})

        return render(request, "inicio.html", {"mensaje": f'Error, formulario invalido'})

    else:

        miFormulario = AuthenticationForm()

        return render(request, "login.html", {"miFormulario": miFormulario})


def register(request):

    print('method:', request.method)
    print('post: ', request.POST)

    if request.method == 'POST':

        miFormulario = UserRegisterForm(request.POST)

        if miFormulario.is_valid():

            username = miFormulario.cleaned_data["username"]

            miFormulario.save()

            return render(request, "inicio.html", {"mensaje": f'Usuario {username} creado con éxito'})

        else:

            return render(request, "inicio.html", {"mensaje": f'Error al crear el usuario'})

    else:

        miFormulario = UserRegisterForm()

        return render(request, "registro.html", {"miFormulario": miFormulario})


def editar_perfil(request):
    
    print('method:', request.method)
    print('post: ', request.POST)

    usuario = request.user

    if request.method == 'POST':

        miFormulario = UserEditForm(request.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data

            usuario.first_name = data["first_name"]
            usuario.last_name = data["last_name"]
            usuario.email = data["email"]
            usuario.set_password(data["password1"])

            usuario.save()

            return render(request, "inicio.html", {"mensaje": f'Datos actualizados!'})
        
        return render(request, "editarPerfil.html", {"mensaje": 'Contraseñas no coinciden'} )
    
    else:

        miFormulario = UserEditForm(instance=request.user)

        return render(request, "editarPerfil.html", {"miFormulario": miFormulario})

