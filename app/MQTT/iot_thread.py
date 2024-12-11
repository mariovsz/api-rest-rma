import threading
from typing import Callable, Optional

import paho.mqtt.client as mqtt


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
        print(f"Conectado con código de resultado {rc}")
        if not self.subscribed:
            client.subscribe(self.topic, qos=1)
            self.subscribed = True
            print("Suscriptor conectado y suscrito!")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        self.message_counter += 1
        if self.message_callback:
            self.message_callback(message)
        else:
            print(f"Mensaje recibido: {msg.topic} {message}")

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, self.keepalive)
        print("Suscriptor iniciado")
        while not self._stop_event.is_set():
            self.client.loop()

    def stop(self):
        print("Finalizando el suscriptor")
        self._stop_event.set()
        self.client.disconnect()
