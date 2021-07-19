from time import sleep
import paho.mqtt.client as mqtt

class mqtt_hassio():
    def __init__(self, _address, _port, _topic) -> None:
        self.address = _address
        self.port = _port
        self.topic = _topic
        self.client = mqtt.Client("ha-client")
        self.client.connect(self.address, self.port)
        self.client.loop_start()
        self.client.publish(self.topic, 'Alive for now...')

    def send_last_event(self, _event):
        self.client.publish(self.topic, _event)
        sleep(0.5)
        self.client.publish(self.topic, 'Dead or Alive')

    def good_bye(self):
        self.client.publish(self.topic, 'Recovering...')