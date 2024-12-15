import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.basemodel import ModeloBase
from .database.database import engine
from .database.nodos.router import router as nodos_router
from .database.paquetes.router import router as paquetes_router
from .database.permisos.router import router as permisos_router
from .database.roles.router import router as roles_router
from .database.tipos.router import router as tipos_router
from .database.users.router import router as user_router
from .MQTT.message_mqtt import on_message
from .MQTT.paho_thread import IoTThread

# Cargar variables de entorno
load_dotenv()
ENV = os.getenv("ENV", "DEV")
ROOT_PATH = os.getenv(f"ROOT_PATH_{ENV.upper()}", "")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "")
MQTT_BROKER = os.getenv("MQTT_BROKER", "")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", 60))


@asynccontextmanager
async def lifespan(app: FastAPI):
    ModeloBase.metadata.create_all(bind=engine)
    # Iniciar el hilo MQTT
    iot_thread = IoTThread(
        MQTT_BROKER,
        MQTT_PORT,
        MQTT_TOPIC,
        MQTT_KEEPALIVE,
        on_message,
    )
    iot_thread.start()

    yield
    # Detener el hilo MQTT
    iot_thread.stop()


# Crear la aplicación FastAPI
app = FastAPI(root_path=ROOT_PATH, lifespan=lifespan)


# Configuración de CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
)


# Incluir rutas
app.include_router(
    paquetes_router,
    prefix="/paquetes",
    tags=["Paquetes"],
)
app.include_router(
    nodos_router,
    prefix="/nodos",
    tags=["Nodos"],
)
app.include_router(
    tipos_router,
    prefix="/tipos",
    tags=["Tipos"],
)
app.include_router(
    permisos_router,
    prefix="/permisos",
    tags=["Permisos"],
)
app.include_router(
    roles_router,
    prefix="/roles",
    tags=["Roles"],
)
app.include_router(
    user_router,
    prefix="/usuarios",
    tags=["Usuarios"],
)
