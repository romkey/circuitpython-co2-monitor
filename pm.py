import board
from adafruit_pm25.i2c import PM25_I2C

def pm_setup():
    global pm25

    i2c = board.I2C()
    pm25 = PM25_I2C(i2c, None)

def pm_loop(values):
    global pm25

    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from PM sensor, retrying...")
        return

    values["pm_03um"] = aqdata["particles 03um"]
    values["pm_05um"] = aqdata["particles 05um"]
    values["pm_10um"] = aqdata["particles 10um"]
    values["pm_25um"] = aqdata["particles 25um"]
    values["pm_50um"] = aqdata["particles 50um"]
    values["pm_100um"] = aqdata["particles 100um"]

    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")
