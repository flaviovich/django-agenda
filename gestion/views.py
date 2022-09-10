from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import (
    ListAPIView, 
    ListCreateAPIView, 
    RetrieveUpdateDestroyAPIView, 
    CreateAPIView)
from .serializers import (
    PruebaSerializer, 
    ImportanciaSerializer, 
    ImportanciaSerializerRUD,
    TareaEtiquetaSerializer, 
    TareaSerializer, 
    TareaConImportanciaSerializer, 
    EtiquetaSerializer)
from .models import Etiqueta, Importancia, Tarea, TareaEtiqueta
from django.db import connection
from datetime import datetime
from rest_framework import status
from pytz import utc

# Create your views here.
@api_view(http_method_names=['GET', 'POST'])
def endpointInicial(request: Request):
    print(request.method)

    if request.method == 'GET':
        return Response(data={
            'message': 'Bienvenido a mi API'
        }, status=200) 
    elif request.method == 'POST':
        print(request.data)
        return Response(data={
            'message': 'Se creo la informacion correctamente'
        })

class PruebaApiView(ListCreateAPIView):
    queryset = [
        {'id': 1, 'nombre': 'Flavio', 'apellido': 'Rios'},
        {'id': 2, 'nombre': 'Juan', 'apellido': 'Perez'}
    ]
    serializer_class = PruebaSerializer

    def post(self, request: Request):
        # sourcery skip: remove-unnecessary-else, swap-if-else-branches
        data = self.serializer_class(data=request.data)
        validacion = data.is_valid()
        print(validacion)
        if validacion == True:
            print(data.validated_data)
            return Response(data={
                'message': 'Prueba creada exitosamente'
            }, status=201)
        else:
            return Response(data={
                'message': 'Error al crear la prueba',
                'content': data.errors
            }, status=400)

class ImportanciasView(ListCreateAPIView):
    queryset = Importancia.objects.all()
    serializer_class = ImportanciaSerializer

    def get_queryset(self):
        return self.queryset.filter(deleted=False).all()

    def get(self, request):
        instancias = self.get_queryset()
        for instancia in instancias:
            print(instancia.nombre)
        data_serializada = self.serializer_class(instance= instancias, many=True)
        # many es para q acepte muchos valores
        return Response({
            'message': 'Las instancias son',
            'content': data_serializada.data
        })
    
    def post(self, request: Request):
        informacion = request.data
        dataASerializar = self.serializer_class(data=informacion)

        dataASerializar.is_valid(raise_exception=True)
        nuevaImportancia = dataASerializar.save()

        # # primera forma
        # infoImportancia = {'nombre':'Ejemplo'}
        # Importancia.objects.create(**infoImportancia)
        # # segunda forma
        # nuevaImportancia = Importancia(**infoImportancia)
        # nuevaImportancia.save()
        return Response({
            'message': 'Importancia creada exitosamente',
            'content': self.serializer_class(instance=nuevaImportancia).data
        }, status=201)

class ImportanciaView(RetrieveUpdateDestroyAPIView):
    queryset = Importancia.objects.all()
    serializer_class=ImportanciaSerializerRUD
    
    def validarImportancia(self, pk):
        resultado = Importancia.objects.filter(id=pk, deleted=False).first()

        if resultado is None:
            return Response(data={
                'message': 'Importancia no existe',
                'content': None
            }, status = 404)
        return resultado
        
    def get(self, request, pk):  # sourcery skip: remove-unnecessary-else
        print(pk)
        resultado = self.validarImportancia(pk)
        if isinstance(resultado, Response):
            return resultado
        else:
            dataSerializada = self.serializer_class(instance=resultado).data
            return Response(data={
                'message': None,
                'content': dataSerializada
            })
    
    def delete(self, request, pk):  # sourcery skip: remove-unnecessary-else
        resultado = self.validarImportancia(pk)
        if isinstance(resultado, Response):
            return resultado
        else:
            resultado.deleted = True
            resultado.save()
            return Response(data={
                'message': 'Importancia eliminada exitosamente',
                'content': None
            })

    def update(self, request, pk):  # sourcery skip: remove-unnecessary-else
        resultado = self.validarImportancia(pk)
        if isinstance(resultado, Response):
            return resultado

        dataSerializada = self.serializer_class(data=request.data)
        dataSerializada.is_valid(raise_exception=True)
        importanciaActualizada = dataSerializada.update(resultado, dataSerializada.validated_data)

        return Response(data={
            'message': 'Importancia actualizada exitosamente',
            'content': self.serializer_class(instance=importanciaActualizada).data
        })

class TareasView(ListCreateAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def post(self, request: Request):
        dataSerializada = self.serializer_class(data=request.data)
        dataSerializada.is_valid(raise_exception=True)
        importancia = dataSerializada.validated_data.get('importancia')

        if importancia.deleted == True:
            return Response(data={
                'message': 'Importancia no existe'
            }, status = 400)

        fechaHoy = utc.localize(datetime.now().utcnow())
        fechaCaducidad = dataSerializada.validated_data.get('fechaCaducidad')
        if fechaHoy > fechaCaducidad:
            return Response(data={
                'message': 'No puede haber tareas con fecha de caducidad menor a la actual'
            }, status = status.HTTP_400_BAD_REQUEST)
        
        nuevaTarea = dataSerializada.save()

        return Response(data={
            'message': 'Tarea creada exitosamente',
            'content': self.serializer_class(instance=nuevaTarea).data
        }, status = status.HTTP_201_CREATED)
    
    def get(self, request: Request):
        tareas = self.get_queryset()
        dataSerializada = TareaConImportanciaSerializer(instance=tareas, many=True)

        return Response(data={
            'message': None,
            'content': dataSerializada.data
        })

class EtiquetasView(ListCreateAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer

class TareaEtiquetasView(CreateAPIView):
    queryset = TareaEtiqueta.objects.all()
    serializer_class = TareaEtiquetaSerializer

@api_view(http_method_names=['GET'])
def usandoVista(self, request):
    cursor = connection.cursor()
    cursor.execute('select * from listar_etiquetas_con_la_letra_A where id = %s and deleted = %s', [4,False])
    respuesta = cursor.fetchall()
    print(respuesta)

    for registro in respuesta:
        diccionario = {
            'id': registro[0],
            'nombre': registro[1],
            'estado': bool(registro[2])
        }
    print(diccionario)

    return Response(data={
        'message': 'Se usó la vista'
    })
