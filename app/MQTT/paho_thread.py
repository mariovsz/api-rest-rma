import threading
from typing import Callable, Optional
from ..config.logging_config import styled_console
from rich.theme import Theme
import paho.mqtt.client as mqtt
import time


class IoTThread(threading.Thread):
    def __init__(
        self,
        broker: str,
        port: int,
        topic: str,
        keepalive: int,
        message_callback: Optional[Callable[[str], None]] = None,
    ):
        super().__init__()
        self._stop_event = threading.Event()
        self.broker = broker
        self.port = port
        self.topic = topic
        self.keepalive = keepalive
        self.client = mqtt.Client()
        self.message_callback = message_callback
        self.message_counter = 0
        self.subscribed = False

    def on_connect(self, client, userdata, flags, rc) -> None:
        if not self.subscribed:
            client.subscribe(self.topic, qos=1)
            self.subscribed = True
            styled_console(
                f"Suscrito al tópico: {self.topic}",
                "MQTT",
            )

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        self.message_counter += 1
        if self.message_callback:
            self.message_callback(message)
        else:
            styled_console(f"Mensaje recibido: {msg.topic} {message}", "MQTT")

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        while not self._stop_event.is_set():
            try:
                self.client.connect(self.broker, self.port, self.keepalive)
                styled_console("Conectado al servicio MQTT", "MQTT")
                self.client.loop_forever()
            except ConnectionRefusedError as e:
                styled_console(f"Error al conectarse al servicio MQTT: {e}", "ERROR")
            except Exception as e:
                styled_console(f"Ocurrió un error inesperado: {e}", "ERROR")
            time.sleep(5)

    def stop(self):
        self._stop_event.set()
        self.client.disconnect()
        self.join()
        styled_console("Finalizando el hilo suscriptor", "MQTT")
