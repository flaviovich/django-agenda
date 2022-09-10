from django.db import models

class Importancia(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=45, unique=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'importancias'

class Tarea(models.Model):
    class CategoriaOpciones(models.TextChoices):
        LISTADO = ('LISTADO', 'LISTADO')
        POR_HACER = ('POR_HACER', 'POR_HACER')
        HACIENDO = ('HACIENDO', 'HACIENDO')
        FINALIZADO = ('FINALIZADO', 'FINALIZADO')
        CANCELADO = ('CANCELADO', 'CANCELADO')

    categoria = models.CharField(choices=CategoriaOpciones.choices, max_length=15, default='LISTADO')
    nombre = models.CharField(max_length=250, null=False)
    descripcion = models.TextField(null=True)
    fechaCaducidad = models.DateTimeField(db_column='fecha_caducidad')
    importancia = models.ForeignKey(to=Importancia, db_column='importancia_id', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'tareas'

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=45, null=False, unique=True)

    class Meta:
        db_table = 'etiquetas'

# https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/
class TareaEtiqueta(models.Model):
    tarea = models.ForeignKey(to=Tarea, db_column='tarea_id', on_delete=models.CASCADE, related_name='tareaEtiqueta')
    etiqueta = models.ForeignKey(to=Etiqueta, db_column='etiqueta_id', on_delete=models.CASCADE, related_name='etiquetaTarea')
    