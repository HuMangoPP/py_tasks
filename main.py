import pygame as pg
from src.components.app import App
from tkinter import Tk, filedialog
import json

def input_dir():
    Tk().withdraw()
    fd = filedialog.askdirectory()
    f = open(f'{fd}/py_tasks.json', 'r')
    data = json.load(f)
    return {
        'data': data,
        'fd': fd
    }

def write_to_json(fd, data):
    f = open(f'{fd}/py_tasks.json', 'w')
    f.write(json.dumps(data, indent=4))

def main(imported_data):
    pg.init()

    res = pg.display.get_desktop_sizes()[0]

    screen = pg.display.set_mode(res)
    pg.display.set_caption('Task Manager')

    clock = pg.time.Clock()

    return App(imported_data, screen, clock).run()


if __name__ == '__main__':
    res = input_dir()
    data = main(res['data'])
    write_to_json(res['fd'], data)
    exit()