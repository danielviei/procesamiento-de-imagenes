# procesamiento-de-imagenes
Procesamiento de imagenes usando Django

## Pre-Requisitos
- Docker
- Docker-compose
- Python

## Instalacion
### Usando Docker
Aqui solo es necesario usar el comando desde la carpeta raiz del proyecto:

```shell
docker-compose --profile all up -d
```

De esta Forma tendremos el servidor corriendo en el puerto 8000

### Sin Docker
Para Rabbimq y la base de datos Postgres se puede usar el siguiente comando para usarlos en Docker

```shell
docker-compose --profile db up -d
```

En el caso de correrlo de forma local es necesario agregar las siguientes variables de entorno para conectarse tanto a la base de datos como con rabbitmq

```shell
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
DATABASE_HOST
DATABASE_PORT

BROKER_URL
```

Debes instalar las dependencias de python

En Linux:
```shell
python -m venv venv
source venv\bin\activate
```

En Windows:

```shell
python -m venv venv
venv\Scripts\activate 
```

Luego podemos iniciar el server

En Linux:
```shell
cd ./images_processing/
python manage.py runserver
```

En Windows:
```shell
cd .\images_processing\
python manage.py runserver
```

De esta forma el server se estará ejecutando en el puerto 8000

Ahora necesitamos iniciar el celery para las tareas asincronas para eso nos matenemos en la carpeta images_processing y ejecutamos:

```shell
celery -A images_processing worker -P gevent -l error
```

## Postman Ejemplos
Para usar los ejemplos de postman es necesario tener instalado Postman y tener 2 imagenes en su working directory. Una debe ser formato jpg llamada image.jpg y una en formato png llamada image.png

Luego de eso puedes importar la collecion que se encuentra en el repo llamado

```shell
Procesamiento de Imagenes.postman_collection.json
```