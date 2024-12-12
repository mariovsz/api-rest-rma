import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.basemodel import ModeloBase
from .database.database import engine
from .database.paquetes.router import router as paquete_router
from .database.nodos.router import router as nodos_router
from .MQTT.iot_thread import IoTThread


# Función callback para procesar mensajes MQTT (opcional)
def process_mqtt_message(message: str):
    print(f"Procesando mensaje: {message}")


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
        process_mqtt_message,
    )
    iot_thread.start()

    yield
    # Detener el hilo MQTT
    iot_thread.stop()
    iot_thread.join()


# Crear la aplicación FastAPI
app = FastAPI(root_path=ROOT_PATH, lifespan=lifespan)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
)


# Incluir rutas
app.include_router(
    paquete_router,
    prefix="/paquetes",
    tags=["Paquetes"],
)
app.include_router(
    nodos_router,
    prefix="/nodos",
    tags=["Nodos"],
)
