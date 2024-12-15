import json
from datetime import datetime
from typing import Optional

from ..database.database import get_db
from ..database.paquetes.schemas import PaqueteCreate
from ..database.paquetes.services import crear_paquete
from ..config.logging_config import styled_console


def es_valido(paquete):
    return True


def guardar_paquete(paquete: PaqueteCreate) -> None:
    crear_paquete(next(get_db()), paquete)
    styled_console(f"Guardado: {paquete}", "MQTT")


def message_validator(msj) -> Optional[PaqueteCreate]:
    msj = msj.replace("'", '"')
    msj_json = json.loads(msj)
    try:
        msj_paquete = {
            "nodo_id": msj_json["id"],
            "type_id": int(msj_json["type"]),
            "data": float(msj_json["data"]),
            "date": datetime.fromtimestamp(msj_json["time"]),
        }
        paquete = PaqueteCreate(**msj_paquete)
        if es_valido(paquete):
            return paquete
    except Exception as e:
        styled_console(f"Error de validación: {e}", "MQTT ERROR")


def on_message(msj: str) -> None:
    paquete = message_validator(msj)
    if paquete is not None:
        guardar_paquete(paquete)
