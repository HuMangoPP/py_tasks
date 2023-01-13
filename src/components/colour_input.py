import pygame as pg
from src.settings import FONT, COLOURS, COLOUR_ARRAY, MARGIN, COLOUR_SELECT_SIZE, HEADER

class ColourInput:
    def __init__(self, desc):
        self.desc = desc
        self.selection = None
        self.w = 500
        self.h = 300
        self.palette = []
        self.create_palette()
    
    def run(self, screen):
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    return (255, 0, 0)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return (255, 0, 0)
                if event.type == pg.MOUSEBUTTONDOWN:
                    for circle in self.palette:
                        x, y = self.to_screen(screen, circle['x'], circle['y'])
                        mx, my = pg.mouse.get_pos()
                        drsq = (mx-x)**2 + (my-y)**2
                        if drsq<=COLOUR_SELECT_SIZE**2:
                            return circle['c']
            self.render(screen)

            pg.display.update()
    
    def to_screen(self, screen, x, y):
        offset_x = x-self.w/2
        offset_y = y-self.h/2
        return screen.get_width()/2+offset_x, screen.get_height()/2+offset_y

    def create_palette(self):
        for i in range(len(COLOUR_ARRAY)):
            row = i//3
            col = i%3
            x = (col-1)*(MARGIN+2*COLOUR_SELECT_SIZE)+self.w/2
            y = row*(MARGIN+2*COLOUR_SELECT_SIZE)+self.h/3
            self.palette.append({
                'x': x,
                'y': y,
                'c': COLOUR_ARRAY[i]
            })

    def render(self, screen):
        surf = pg.Surface((self.w, self.h))
        surf.fill(COLOURS['i_hdr'])
        FONT.render(surf, self.desc, self.w/2, HEADER/2, COLOURS['fc'], 12, 'center')
        pg.draw.rect(surf, COLOURS['i_bg'], (0, HEADER, self.w, self.h-HEADER))

        for circle in self.palette:
            pg.draw.circle(surf, circle['c'], (circle['x'], circle['y']), COLOUR_SELECT_SIZE)

        screen.blit(surf, (screen.get_width()/2-self.w/2, screen.get_height()/2-self.h/2))