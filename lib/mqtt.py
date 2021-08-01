from time import sleep, time
import paho.mqtt.client as mqtt
from lib import config, debug, timeout

CONNECTION_STATUS = ["connected", "disconnected", "trying"]

class mqtt_hassio():
    def __del__(self):
        self._do_disconnect()
        sleep(1)

    def __init__(self, _address, _port, _topic) -> None:
        self.address = _address
        self.port = _port
        self.topic = _topic
        self.qos = 1
        self.client = mqtt.Client("ha-client")
        self.client.on_publish = self._on_publish
        self.client.on_disconnect = self._on_disconnect
        self.client.on_connect = self._on_connect
        self.client.username_pw_set(config.wzHassioUser, config.wzHassioPassword)
        self.client.loop_start()
        self._do_publish("Alive for now...")
        sleep(0.5)


    #######################################
    # Publish function
    #######################################
    def _do_publish(self, msg):
        try:
            self._publish(msg)
        except:
            debug.dbgPrint("Could not publish data")

    @timeout.exit_after(5)
    def _publish(self, msg):
        if not self.client.is_connected():
            debug.dbgPrint("Not connected, will do it now")
            self._do_connect()
        ret = self.client.publish(self.topic, msg, qos=self.qos)
        debug.dbgPrint("Publish ret:", ret)
        while not ret.is_published():
            sleep(0.1)


    #######################################
    # Conection and Disconnection functions
    #######################################
    def _do_connect(self):
        try:
            self._connect()
        except:
            debug.dbgPrint("Error on connection")

    @timeout.exit_after(5)
    def _connect(self):
        self.client.connect(self.address, self.port)
        while not self.client.is_connected():
            sleep(0.1)

    def _do_disconnect(self):
        try:
            self._disconnect()
        except:
            debug.dbgPrint("Error on disconnection")

    @timeout.exit_after(3)
    def _disconnect(self):
        self.client.disconnect()
        while self.client.is_connected():
            sleep(0.1)


    #######################################
    # Handlers
    #######################################
    def _on_disconnect(self, client, userdata, rc):
        debug.dbgPrint("Disconnected from server", client, userdata, rc)

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        debug.dbgPrint("Connected to server!", client, userdata, flags, rc)
        pass

    def _on_publish(self, client,userdata,result):
        debug.dbgPrint(client, userdata, result, "data published!")
        pass


    #######################################
    # Public functions
    #######################################
    def send_last_event(self, _event):
        self._do_publish(_event)
        sleep(0.5)
        self._do_publish('Dead or Alive')

    def good_bye(self):
        self._do_publish('Recovering...')
        self._do_disconnect()
