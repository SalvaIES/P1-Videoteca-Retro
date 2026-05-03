from django.urls import path
from . import views

urlpatterns = [
    path('', views.coleccion, name='coleccion'),
    path('añadir/', views.añadir_juego, name='añadir_juego'),
    path('editar/<int:id_juego>/', views.editar_juego, name='editar_juego'),
    path('eliminar/<int:id_juego>/', views.eliminar_juego, name='eliminar_juego'),
    path('prestar/<int:id_juego>/', views.prestar_juego, name='prestar_juego'),
    path('devolver/<int:id_juego>/', views.devolver_juego, name='devolver_juego'),
    path('analisis/', views.analisis, name='analisis'),
]
