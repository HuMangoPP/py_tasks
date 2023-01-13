import pygame as pg
from src.settings import FONT, FONT_SIZE, COLOURS

class Button:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.surf = pg.Surface((w, h))
        self.text = text

    def update_rect(self, new):
        x = new['x'] if 'x' in new else self.rect.left
        y = new['y'] if 'y' in new else self.rect.top
        w = new['w'] if 'w' in new else self.rect.width
        h = new['h'] if 'h' in new else self.rect.height
        self.rect = pg.Rect(x, y, w, h)
        self.surf = pg.Surface((w, h))

    def render(self, screen):
        FONT.render(self.surf, self.text, self.rect.width/2, self.rect.height/2, COLOURS['fc'], FONT_SIZE, style='center')
        screen.blit(self.surf, self.rect)
    
    def hover(self, c_idle, c_hover):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.surf.fill(c_hover)
        else:
            self.surf.fill(c_idle)
    
    def click(self, cb, events):
        # check if button is clicked
        # call the cb function
        if self.rect.collidepoint(pg.mouse.get_pos()):
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    cb()
                    return True
        return False
