from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Etiqueta, Importancia, Tarea, TareaEtiqueta

class PruebaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(required=True, trim_whitespace=True, max_length=20)
    apellido = serializers.CharField(required=True, trim_whitespace=True, max_length=15)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        print('Aca se deberia guardar la info en la BD')
        print(validated_data)
        return

class ImportanciaSerializer(serializers.ModelSerializer):

    def save(self):
        # sourcery skip: inline-immediately-returned-variable
        self.validated_data['nombre'] = self.validated_data.get('nombre').lower()
        nuevaImportancia = Importancia.objects.create(**self.validated_data)
        return nuevaImportancia
        
    class Meta:
        model = Importancia
        # fields = ['id', 'nombre']
        exclude = ['deleted']

class ImportanciaSerializerRUD(serializers.ModelSerializer):
    class Meta:
        model = Importancia 
        # fields = '__all__'
        exclude = ['deleted']

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

class ImportanciaSinDeletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Importancia
        exclude = ['deleted']

class TareaEtiquetaConEtiquetasSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareaEtiqueta
        exclude = ['tarea','id']
        depth = 1

class TareaConImportanciaSerializer(serializers.ModelSerializer):
    importancia = ImportanciaSinDeletedSerializer()
    etiquetas = TareaEtiquetaConEtiquetasSerializer(many=True, source='tareaEtiqueta')

    class Meta:
        model = Tarea
        fields = '__all__'
        # depth = 1 # nested serializer

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'

class TareaEtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareaEtiqueta
        fields = '__all__'
