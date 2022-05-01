import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

try:
    from secrets import secrets
except ImportError:
    print("Homebus secrets are kept in secrets.py, please add them there!")
    raise

def _connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT broker! Listening for topic changes on %s" % default_topic)
    # Subscribe to all changes on the default_topic feed.
    client.subscribe(default_topic)


def _disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker!")


def _message(client, topic, message):
    """Method callled when a client's subscribed feed has a new
    value.
    :param str topic: The topic of the feed with a new value.
    :param str message: The new value
    """
    print("New message on topic {0}: {1}".format(topic, message))

def homebus_setup():
    global mqtt_client

    pool = socketpool.SocketPool(wifi.radio)
    mqtt_client = MQTT.MQTT(
        broker=secrets["homebus_broker"],
        port=secrets["homebus_port"],
        username=secrets["homebus_username"],
        password=secrets["homebus_password"],
        socket_pool=pool,
        ssl_context=ssl.create_default_context(),
    )

    mqtt_client.on_connect = _connected
    mqtt_client.on_disconnect = _disconnected
    mqtt_client.on_message = _message

    print("Connecting to MQTT broker...")
    mqtt_client.connect()

def homebus_loop(values):
    global mqtt_client

    mqtt_client.loop()
