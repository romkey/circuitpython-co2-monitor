import board
import adafruit_bme680

def temperature_setup():
    global bme680

    i2c = board.I2C()
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    bme680.sea_level_pressure = 1013.25

def temperature_loop(values):
    global bme680

    values["temperature"] = bme680.temperature
    values["humidity"] = bme680.humidity
    values["pressure"] = bme680.pressure
    values["voc"] = bme680.gas

    print("\nTemperature: %0.1f C" % bme680.temperature)
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)
