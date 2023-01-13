from src.font import Font
import pygame as pg

FONT = Font(pg.image.load('./assets/font/font.png'))
FONT_SIZE = 12
FPS = 60
MARGIN = 10
PAD = 10
HEADER = 50
BTN_SIZE = 30
COLOURS = {
    'fc': (255, 255, 255),
    'ts_bg': (50, 50, 50),
    'i_bg': (50, 50, 50),
    't_hvr': (100, 100, 100),
    't_idle': (75, 75, 75),
    'ts_btn_idle': (100, 100, 100),
    'ts_btn_hvr': (125, 125, 125),
    'i_hdr': (25, 25, 25),
}
COLOUR_ARRAY = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]
COLOUR_SELECT_SIZE = 30