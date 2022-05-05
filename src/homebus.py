import socketpool
import wifi
import ssl
from real_ntp import NTP
import time
import json
import gc

import adafruit_requests as requests

import adafruit_minimqtt.adafruit_minimqtt as MQTT

class Homebus:
    def __init__(self, broker, port, username, password, id):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.id = id

    def _connected(client, userdata, flags, rc):
        # This function will be called when the client is connected
        # successfully to the broker.
        print("Connected to Homebus broker!")

    def _disconnected(client, userdata, rc):
        # This method is called when the client is disconnected
        print("Disconnected from Homebus Broker!")


    def _message(client, topic, message):
        """Method callled when a client's subscribed feed has a new
        value.
        :param str topic: The topic of the feed with a new value.
        :param str message: The new value
        """
        print("New message on topic {0}: {1}".format(topic, message))

    def _provision():
        socket = socketpool.SocketPool(wifi.radio)
        https = requests.Session(socket, ssl.create_default_context())        

        request = {}
        request["consumes"] = self.consumes
        request["publishes"] = self.publishes
        request["identity"] = self.identity

        response = https.post(self.provisioning_url, request)

    def setup(self):
        pool = socketpool.SocketPool(wifi.radio)
        self.mqtt_client = MQTT.MQTT(
            broker=self.broker,
            port=self.port,
            username=self.username,
            password=self.password,
            socket_pool=pool,
            ssl_context=ssl.create_default_context()
            )

        self.mqtt_client.on_connect = Homebus._connected
        self.mqtt_client.on_disconnect = Homebus._disconnected
        self.mqtt_client.on_message = Homebus._message
        self.update_interval = 60

        self.ntp = NTP(pool)
        self.ntp.datetime

        print("Connecting to MQTT broker...")
        self.mqtt_client.connect()

        self.next_update = time.time()

    def _homebus_publish(self, ddc, data):
        url = "homebus/device/" + self.id + "/" + ddc
        msg = json.dumps({ "source": self.id,
#                           "timestamp": time.time(),
                           "timestamp": self.ntp.datetime,
                           "contents": {
                               "ddc": ddc,
                               "payload": data
                               }})

        print("\n")
        print(url)
        print(msg)
        print("\n")
        print("\n")

        self.mqtt_client.publish(url, msg)

    def loop(self, values):
        self.mqtt_client.loop()

        print("Memory Info - gc.mem_free()")
        print("---------------------------")
        print("{} Bytes\n".format(gc.mem_free()))

        if self.next_update < time.time():
            self.next_update += self.update_interval

            url = "homebus/device/" + self.id

            if values["temperature"] != None and values["humidity"] and values["pressure"]:
                data = {
                    "temperature": values["temperature"],
                    "humidity": values["humidity"],
                    "pressure": values["pressure"]
                    }

                self._homebus_publish("org.homebus.experimental.air-sensor", data)

            if values["voc"] != None:
                data = {
                    "voc": values["voc"]
                    }
                self._homebus_publish("org.homebus.experimental.voc-sensor", data)

            if values["co2"] != None:
                data = {
                    "co2": values["co2"]
                    }
                self._homebus_publish("org.homebus.experimental.co2-sensor", data)

            if values["pm_03um"] != None and values["pm_05um"] != None and values["pm_10um"] != None and values["pm_25um"] != None and values["pm_50um"] != None and values["pm_100um"] != None:
                data = {
                    "pm03": values["pm_03um"],
                    "pm05": values["pm_05um"],
                    "pm1":  values["pm_10um"],
                    "pm25": values["pm_25um"],
                    "pm10": values["pm_100um"]
                    }
                self._homebus_publish("org.homebus.experimental.air-quality-sensor", data)
