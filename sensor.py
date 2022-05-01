import time
# from wifi import *
from temperature import *
from co2 import *
from pm import *
from display import *
from homebus import *

def do_it(interval = 60):
    # wifi_setup()
    temperature_setup()
    co2_setup()
    pm_setup()
    display_setup()
    # homebus_setup()

    values = {
        "temperature": None,
        "humidity": None,
        "pressure": None,
        "voc": None,
        "co2": None
        }

    while True:
        temperature_loop(values)
        co2_loop(values)
        pm_loop(values)
        display_loop(values)
        # homebus_loop(values)
        time.sleep(interval)
