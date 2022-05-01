import board
import displayio

import adafruit_displayio_ssd1306
import adafruit_bus_device

from adafruit_display_text import label
import terminalio

def setup_display():
    global ssd1306

    displayio.release_displays()
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3d)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

    # Make the display context
    splash = displayio.Group()
    display.show(splash)

    color_bitmap = displayio.Bitmap(128, 128, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFF0000

    bg_sprite = displayio.TileGrid(color_bitmap,
                                pixel_shader=color_palette,
                                x=0, y=0)
    splash.append(bg_sprite)

    text = "Hello World!"
    text_area = label.Label(
        terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
        )
    splash.append(text_area)

def display_loop(values):
    global ssd1306

    text = "CO2 % s" % values["co2"]
