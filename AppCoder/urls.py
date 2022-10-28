from django.urls import path

from .views import CursoCreate, CursoDelete, CursoDetail, CursoList, CursoUpdate, buscar, busquedaCamada, crea_profesor, curso, cursoFormulario, cursos, editar_profesor, eliminarProfesor, entregables, estudiantes, inicio, lista_curso, listaProfesores, profesores


urlpatterns = [
    path('agrega-curso/<nombre>/<camada>', curso),
    path('', inicio, name='Inicio'),
    path('lista-cursos/', lista_curso),
    path('cursos/', cursos, name="Cursos"),
    path('profesores/', profesores, name="Profesores"),
    path('estudiantes/', estudiantes, name="Estudiantes"),
    path('entregables/', entregables, name="Entregables"),
    path('cursoFormulario/', cursoFormulario, name="CursoFormulario"),
    path('busquedaCamada/', busquedaCamada, name="BusquedaCamada"),
    path('buscar/', buscar, name="Buscar"),
    path('listaProfesores/', listaProfesores, name="ListaProfesores"),
    path('crea-profesor/', crea_profesor, name="CreaProfesor"),
    path('elimina-profesor/<int:id>', eliminarProfesor, name="EliminaProfesor"),
    path('editar-profesor/<int:id>', editar_profesor, name="EditarProfesor"),
    path('listaCursos', CursoList.as_view(), name="ListaCursos"),
    path('detalleCurso/<pk>', CursoDetail.as_view(), name="DetalleCurso"),
    path('creaCurso/', CursoCreate.as_view(), name="CreaCurso"),
    path('actualizarCurso/<pk>', CursoUpdate.as_view(), name="ActualizaCursos"),
    path('eliminarCurso/<pk>', CursoDelete.as_view(), name="EliminaCursos"),
]
