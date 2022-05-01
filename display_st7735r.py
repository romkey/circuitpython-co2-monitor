import board
from adafruit_st7735r import ST7735R

def display_setup():
    global display_st7735r

    spi = board.SPI()
    tft_cs = board.D5
    tft_dc = board.D6
    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D9)
    display = ST7735R(display_bus, width=128, height=128, colstart=2, rowstart=1)

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
    global display_st7735r
