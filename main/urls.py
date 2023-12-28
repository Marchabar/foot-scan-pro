from django.contrib import admin
from django.urls import path, include
from main import views
from main import populate


urlpatterns = [
    path('', views.index),
    path('cargar-db/', populate.cargar, name='cargar-db'),
    path('listado-equipos/', views.listado_equipos, name='listado-equipos'),
    path('listado-jornadas/', views.listado_jornadas, name='listado-jornadas'),
    path('listado-jornadas/partidos/<int:id_jornada>/', views.listado_partidos_jornada, name='listado-partidos-jornada'),
    path('listado-jugadores/', views.listado_jugadores, name='listado-jugadores'),
    
]