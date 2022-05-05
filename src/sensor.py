import time
# from wifi import *
from temperature import *
from co2 import *
from pm import *
from display import *
from homebus import *

import adafruit_dotstar
import board
import feathers2

try:
    from secrets import secrets
except ImportError:
    print("Wifi secrets are kept in secrets.py, please add them there!")
    raise

def do_it(interval = 60):
    print("Connecting to %s" % secrets["wifi_ssid"])
    wifi.radio.connect(secrets["wifi_ssid"], secrets["wifi_password"])
    print("Connected to %s!" % secrets["wifi_ssid"])

    pool = socketpool.SocketPool(wifi.radio)

    temperature_setup()
    co2_setup()
    pm_setup()
    display_setup()

    homebus = Homebus(secrets["homebus_broker"],
                      secrets["homebus_port"],
                      secrets["homebus_username"],
                      secrets["homebus_password"],
                      secrets["homebus_device_id"])
    homebus.setup()

    values = {
        "temperature": None,
        "humidity": None,
        "pressure": None,
        "voc": None,
        "co2": None,
        "pm03": None,
        "pm05": None,
        "pm1":  None,
        "pm25": None,
        "pm10": None
        }

    dotstar = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.5, auto_write=True)
    color_index = 0

    while True:
        temperature_loop(values)
        co2_loop(values)
        pm_loop(values)
        display_loop(values)
        homebus.loop(values)

        time_to_stop = time.time() + interval
        while(time.time() < time_to_stop):
            # Get the R,G,B values of the next colour
            r,g,b = feathers2.dotstar_color_wheel( color_index )
            dotstar[0] = ( r, g, b, 0.5)
            color_index += 1
    
            if color_index == 255:
                color_index = 0
                feathers2.led_blink()

            time.sleep(0.15)
