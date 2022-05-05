import board
import displayio

import adafruit_displayio_ssd1306
import adafruit_bus_device

from adafruit_display_text import label
import terminalio

def display_setup():
    global ssd1306, _display, splash

    displayio.release_displays()
    i2c = board.I2C()
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3d)
    _display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

    # Make the display context
    splash = displayio.Group()
    _display.show(splash)

    color_bitmap = displayio.Bitmap(128, 64, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFF0000

    bg_sprite = displayio.TileGrid(color_bitmap,
                                pixel_shader=color_palette,
                                x=0, y=0)
    splash.append(bg_sprite)

    text = "Hello World!"
    text_area = label.Label(
        terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=20 // 2 - 1
        )
    splash.append(text_area)

def display_clear():
    color_bitmap = displayio.Bitmap(128, 64, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFF0000

    bg_sprite = displayio.TileGrid(color_bitmap,
                                pixel_shader=color_palette,
                                x=0, y=0)
    splash.append(bg_sprite)

def display_loop(values):
    global ssd1306, _display, splash

    display_clear()

    lines = []

    if values["co2"] != None:
        lines.append("CO2 % s" % values["co2"])

    if values["temperature"] != None:
        lines.append("tmp % s" % values["temperature"])

    if values["humidity"] != None:
        lines.append("hum %s" % values["humidity"])

    if values["pressure"] != None:
        lines.append("prs %s" % values["pressure"])

    text = "\n".join(lines)

    text_area = label.Label(
        terminalio.FONT, text=text, color=0xFFFFFF, x=5, y=10 // 2 - 1
        )
    splash.append(text_area)
