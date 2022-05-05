import board
import adafruit_scd4x

def co2_setup():
    global scd4x

    i2c = board.I2C()
    scd4x = adafruit_scd4x.SCD4X(i2c)
    print("SCD4x serial number:", [hex(i) for i in scd4x.serial_number])
    scd4x.start_periodic_measurement()

def co2_loop(values):
    global scd4x

    if scd4x.data_ready:
        values["co2"] = scd4x.CO2
        values["temperature"] = scd4x.temperature
        values["humidity"] = scd4x.relative_humidity

        print("CO2: %d ppm" % scd4x.CO2)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()
