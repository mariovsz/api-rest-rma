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

Este proyecto permite monitorear diversas condiciones ambientales a través de nodos IoT desplegados en una red. Los nodos recopilan datos como temperatura, humedad, calidad del aire, entre otros, y los envían a una base de datos central para su almacenamiento y análisis.

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
