import pygame as pg
from src.components.button import Button
from src.components.input import Input
from src.settings import FONT, MARGIN, PAD, BTN_SIZE, FONT_SIZE, COLOURS

class Task:
    def __init__(self, desc, w, x, y):
        width = w-2*MARGIN
        text_width = width-BTN_SIZE
        height = FONT.text_height(desc, FONT_SIZE, width=text_width-2*PAD)+2*PAD
        self.rect = pg.Rect(x, y, text_width, height)
        self.surf = pg.Surface((width, height))
        self.desc = desc
        self.being_dragged = False
        self.drag_x = 0
        self.drag_y = 0
        self.edit_btn = Button(x+width-BTN_SIZE, y, BTN_SIZE, height/2, '')
        self.rmv_btn = Button(x+width-BTN_SIZE, y+height/2, BTN_SIZE, height/2, '')
    
    def click_edit_btn(self, screen, events):
        self.edit_btn.click(lambda : self.update_desc(Input('edit task').run(screen)), events)

    def click_delete_btn(self, events):
        return self.rmv_btn.click(lambda : None, events)

    def update_desc(self, desc):
        self.desc = desc
        text_width = self.rect.width-BTN_SIZE
        height = FONT.text_height(desc, FONT_SIZE, width=text_width-2*PAD)+2*PAD
        self.rect = pg.Rect(self.rect.left, self.rect.top, self.rect.width, height)
        self.surf = pg.Surface((self.surf.get_width(), height))
        
        self.edit_btn.update_rect({
            'x': self.rect.left+self.surf.get_width()-BTN_SIZE,
            'y': self.rect.top,
            'w': BTN_SIZE,
            'h': height/2,
        })
        self.rmv_btn.update_rect({
            'x': self.rect.left+self.surf.get_width()-BTN_SIZE,
            'y': self.rect.top+height/2,
            'w': BTN_SIZE,
            'h': height/2,
        })

    def update_pos(self, x, y):
        if not self.being_dragged:
            self.rect.left = x+MARGIN
            self.rect.top = y
            
            width = self.surf.get_width()
            height = self.rect.height
            self.edit_btn.update_rect({
                'x': self.rect.left+width-BTN_SIZE, 
                'y': self.rect.top
            })
            self.rmv_btn.update_rect({
                'x': self.rect.left+width-BTN_SIZE, 
                'y': self.rect.top+height/2
            })

    def hover(self):
        return self.rect.collidepoint(pg.mouse.get_pos())
    
    def drag(self):
        # task already being dragged
        if self.being_dragged:
            self.surf.fill(COLOURS['t_hvr'])
            x, y = pg.mouse.get_pos()
            self.rect.left = x-self.drag_x
            self.rect.top = y-self.drag_y

            self.edit_btn.update_rect({
                'x': self.rect.left+self.rect.width-BTN_SIZE, 
                'y': self.rect.top
            })
            self.rmv_btn.update_rect({
                'x': self.rect.left+self.rect.width-BTN_SIZE, 
                'y': self.rect.top+self.rect.height/2
            })
        # task begin dragging
        else:
            x, y = pg.mouse.get_pos()
            self.drag_x = x+MARGIN-self.rect.left
            self.drag_y = y-self.rect.top
            self.being_dragged = True
        
    def drop(self):
        # stop being dragged
        self.being_dragged = False

    def render(self, screen):
        if self.hover():
            self.surf.fill(COLOURS['t_hvr'])
        else:
            self.surf.fill(COLOURS['t_idle'])
        FONT.render(self.surf, self.desc, 
                    FONT_SIZE/2+PAD, FONT.char_height(FONT_SIZE)/2+PAD,
                    COLOURS['fc'], FONT_SIZE, box_width=self.rect.width-2*PAD)
        screen.blit(self.surf, self.rect)
        self.edit_btn.hover((255, 255, 0), (200, 200, 0))
        self.edit_btn.render(screen)
        self.rmv_btn.hover((255, 0, 0), (200, 0, 0))
        self.rmv_btn.render(screen)
        