import pygame as pg
from src.settings import FONT, MARGIN, COLOURS

class Input:
    def __init__(self, desc):
        self.desc = desc
        self.field = ''
        self.w = 500
        self.h = 300
    
    def run(self, screen):
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    return self.field
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return self.field
                    elif event.key == pg.K_RETURN:
                        return self.field
                    elif event.key == pg.K_BACKSPACE:
                        # check if can delete
                        if self.field:
                            self.field = self.field[:len(self.field)-1]
                    else:
                        # check if char is in the font
                        char = chr(event.key)
                        if char in FONT.char_key or char==' ':
                            self.field+=chr(event.key)
            
            self.render(screen)

            pg.display.update()

    
    def render(self, screen):
        surf = pg.Surface((self.w, self.h))
        surf.fill((25, 25, 25))
        FONT.render(surf, self.desc, 250, 25, COLOURS['fc'], 12, 'center')
        pg.draw.rect(surf, COLOURS['i_bg'], (0, 60, 500, 240))
        FONT.render(surf, self.field, 10, 70, (255, 255, 255), 12, box_width=self.w-2*MARGIN)
        screen.blit(surf, (screen.get_width()/2-250, screen.get_height()/2-150))