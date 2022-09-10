from django.urls import path
from .views import (
    EtiquetasView,
    TareaEtiquetasView,
    endpointInicial, 
    PruebaApiView, 
    ImportanciasView, 
    ImportanciaView, 
    TareasView,
    usandoVista)

urlpatterns = [
    path('inicio', endpointInicial),
    path('prueba', PruebaApiView.as_view()),
    path('importancias', ImportanciasView.as_view()),
    path('importancia/<int:pk>', ImportanciaView.as_view()),
    path('tareas', TareasView.as_view()),
    path('prueba-view-bd', usandoVista),
    path('etiquetas', EtiquetasView.as_view()),
    path('tarea-etiqueta', TareaEtiquetasView.as_view())
]