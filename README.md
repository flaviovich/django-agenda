# Introduccion a flask

## Creamos entorno virtual con python 

- Para crear el entorno virual se usa el comando: 
```bash
    python -m venv venv
```
- Para activar el entorno virtual se usa el comando ("bin" en MAC y "Scripts" en Windows):
```bash
    source venv/bin/activate
```
```bash
    source venv/Scripts/activate
```
- Para desactivar el entorno virtual se usa el comando:
```bash
    deactivate
```

## Instalamos flask
- Para instalar flask se usa el comando:
```bash
    pip install flask
```
- Para ver las librerias instaladas se usa el comando:
```bash
    pip freeze
```
```bash
    pip list
```

## Levantamos el servidor
- Para levantar el servidor se usa el comando:
```bash
    flask run
```
- Para levantar el servidor en modo debug se usa el comando:
```bash
    flask --debug run
```

# Crear una API con flask y sqlalchemy
- Primero tenemos que instalar las librerias:
```bash
    pip install flask-sqlalchemy
```

# Creamos un ecommerce con flask y marshmallow
- Instalamos las dependencias de nuestro requirements.txt:
```bash
    pip install -r requirements.txt
```
- O instalamos las librerias de forma manual:
```bash
    pip install flask
    pip install flask-sqlalchemy
    pip install flask-cors
    pip install flask-migrate
    pip install flask-marshmallow
    pip install marshmallow-sqlalchemy
```
- Luego de crear nuestros modelos vamos a migrar la base de datos (SOLO SE EJECUTA UNA SOLA VEZ):
```bash
    flask db init
```
- Luego de migrar la base de datos vamos a crear la base de datos:
```bash
    flask db migrate -m "Initial migration"
```
- Luego de crear la base de datos vamos a hacer el rollback:
```bash
    flask db upgrade
```

# Nuestras variables de entorno (Necesario para que funcione)
```text
FLASK_DEBUG=True
FLASK_RUN_PORT=5000
# FLASK_APP='main.py'
FLASK_RUN_HOST=127.0.0.1

DB_URI=mysql://root:root@localhost/flask_ecommerce
```


```bash
django-admin startproject agenda
python manage.py startapp gestion
python manage.py runserver
python manage.py showmigrations
pip install mysqlclient
python manage.py migrate
python manage.py makemigrations gestion --name migracion_inicial
python manage.py sqlmigrate gestion 0001
pip install djangorestframework
python manage.py shell
pip install whitenoise
python manage.py collectstatic
heroku login
heroku logs --tail --app agenda-flavio-rios
pip install gunicorn
pip install python-dotenv
```
```text
# Relaciones
# on_delete > significa que va a suceder cuando se intente eliminar una importancia que tiene tareas
# CASCADE > primero eliminara la Importancia y luego eliminara todas las Tareas de esa importancia
# PROTECT > evitara la eliminacion de la Importancia mientras que tenga Tareas ProtectError
# RESTRICT > evitara la eliminacion pero emitira un error de tipo RestrictedError
# SET_NULL > eliminara la Importancia pero todas las tareas de esa importancia las seteara en 'null'
# SET_DEFAULT > eliminara la Importancia pero tendremos que indicar un valor por defecto para que sea reemplazado
# DO_NOTHING > No toma ninguna accion, elimina la Importancia pero aun conservara ese ID eliminado (es el mas peligroso de todos porque puede generar mala incongruencia de datos)
```