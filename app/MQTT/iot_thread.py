import threading
from typing import Callable, Optional
from ..config.logging_config import get_rich_toolkit
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
        self.toolkit = get_rich_toolkit()
        self.toolkit.print_line()

    def on_connect(self, client, userdata, flags, rc) -> None:
        if not self.subscribed:
            client.subscribe(self.topic, qos=1)
            self.subscribed = True
            self.toolkit.print(
                f"Suscrito al tópico: {self.topic}",
                tag="MQTT",
            )

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        self.message_counter += 1
        if self.message_callback:
            self.message_callback(message)
        else:
            self.toolkit.print(f"Mensaje recibido: {msg.topic} {message}", tag="MQTT")

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        while not self._stop_event.is_set():
            try:
                self.client.connect(self.broker, self.port, self.keepalive)
                self.toolkit.print("Conectado al servicio MQTT", tag="MQTT")
                self.client.loop_forever()
            except ConnectionRefusedError as e:
                self.toolkit.print(
                    f"Error al conectarse al servicio MQTT: {e}", tag="MQTT"
                )
            except Exception as e:
                self.toolkit.print(f"Ocurrió un error inesperado: {e}", tag="MQTT")
            time.sleep(5)

    def stop(self):
        self.toolkit.print("Finalizando el suscriptor", tag="MQTT")
        self._stop_event.set()
        self.client.disconnect()
