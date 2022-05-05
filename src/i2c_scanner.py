import time
import board

def i2c_scanner():
    i2c = board.I2C()

    # To create I2C bus on specific pins
    # import busio
    # i2c = busio.I2C(board.SCL1, board.SDA1)  # QT Py RP2040 STEMMA connector
    # i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

    i2c.try_lock()
    print(
        "I2C addresses found:",
        [hex(device_address) for device_address in i2c.scan()],
    )

    i2c.unlock()
