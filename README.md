# API REST RMA

El proyecto consiste en una API REST para gestionar un sistema de Nodos IoT. La API permite la interacción con los nodos, la recolección de datos en tiempo real y el análisis de los mismos.

## Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Instalación](#instalación)
<!-- - [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
  -->

## Descripción

Este proyecto permite monitorear diversas condiciones ambientales a través de nodos IoT desplegados en una red. Los nodos recopilan datos como temperatura, humedad, viento, entre otros, y los envían a una base de datos central para su almacenamiento y análisis.

## Características

- Gestión de Nodos IoT (registro, actualización, eliminación)
- Recolección y almacenamiento de datos en tiempo real
- Consultas de datos históricos
- Integración con PostgreSQL
- Implementación de Docker para un despliegue fácil y rápido

### Requisitos

- **Docker** y **Docker Compose** instalados
- **Python 3.8+**

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/mariovsz/api-rest-rma.git
cd api-rest-rma

# Crear y activar un entorno virtual
python -m venv env
source env/bin/activate

# En Windows usá
env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear y ejecutar el contenedor de Docker
docker-compose up -d
```

```.
├── app
│ ├── database.py # Configuración de la base de datos
│ ├── main.py # Punto de entrada de la aplicación
│ ├── entidad
│ | ├── models.py #modelo de las entidades
│ | ├── schemas.py # Esquemas Pydantic para validación de datos
│ | ├── router.py # Rutas de la API
│ | └── services.py # servicios para las operaciones CRUD
│ ├── MQTT
│ ├── AUTH
│ └──
├── Dockerfile # Dockerfile para construir la imagen
├── docker-compose.yml # Configuración de Docker Compose
├── .env # Archivo de variables de entorno
├── requirements.txt # Dependencias del proyecto
└── README.md # Este archivo
```

```Representación de la base de datos en dbdiagram.io

table Nodos {
  id int [pk, increment]
  nombre varchar(255)
  ubicacion varchar(255)
  tipo_sensor varchar(255)
  estado varchar(50)
}

table Paquetes {
  id int [pk, increment]
  nodo_id int [ref: > Nodos.id]
  tipo_id int [ref: > Tipos.id]
  valor float
  timestamp datetime
}

table Permisos {
  id int [pk, increment]
  nombre varchar(255)
  descripcion varchar(255)
}

table Roles {
  id int [pk, increment]
  nombre varchar(255)
  descripcion varchar(255)
}

table RolePermisos {
  rol_id int [ref: > Roles.id]
  permiso_id int [ref: > Permisos.id]
}

table Tipos {
  id int [pk, increment]
  nombre varchar(255)
  simbolo varchar(50)
}

table Usuarios {
  id int [pk, increment]
  nombre varchar(255)
  email varchar(255)
  hashed_password varchar(255)
}

table UserRoles {
  usuario_id int [ref: > Usuarios.id]
  rol_id int [ref: > Roles.id]
}

table Alarmas {
  id int [pk, increment]
  nodo_id int [ref: > Nodos.id]
  umbral_id int [ref: > Umbrales.id]
  tipo varchar(255)
  fecha datetime
}

table Notificaciones {
  id int [pk, increment]
  alarma_id int [ref: > Alarmas.id]
  usuario_id int [ref: > Usuarios.id]
  mensaje varchar(255)
  fecha datetime
}

table Umbrales {
  id int [pk, increment]
  tipo_id int [ref: > Tipos.id]
  valor_min float
  valor_max float
  descripcion varchar(255)
}
```
