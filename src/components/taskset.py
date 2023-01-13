import pygame as pg
from src.components.task import Task
from src.components.button import Button
from src.components.input import Input
from src.settings import MARGIN, FONT, HEADER, BTN_SIZE, COLOURS, FONT_SIZE

class TaskSet:
    def __init__(self, c, name, tasks, x, y, w=300, h=500):
        self.c = c
        self.name = name
        self.tasks = tasks
        self.rect = pg.Rect(x, y, w, h)
        self.surf = pg.Surface((w, h))
        self.w = w
        self.h = h
        self.add_btn = Button(0, 0, w, BTN_SIZE, 'Add New Task')
        self.rmv_btn = Button(w-BTN_SIZE, y, BTN_SIZE, BTN_SIZE, 'x')
    
    def render(self, screen):
        # background color + header color
        self.surf.fill(COLOURS['ts_bg'])
        pg.draw.rect(self.surf, self.c, (0, 0, self.w, HEADER))
        FONT.render(self.surf, self.name, self.surf.get_width()/2, HEADER/2, COLOURS['fc'], FONT_SIZE, 'center')
        
        # box
        screen.blit(self.surf, self.rect)

        # add btn
        self.add_btn.update_rect({
            'x': self.rect.left, 
            'y': self.rect.top+self.h-self.add_btn.rect.height, 
        })
        self.add_btn.hover(COLOURS['ts_btn_idle'], COLOURS['ts_btn_hvr'])
        self.add_btn.render(screen)

        # remove btn
        self.rmv_btn.update_rect({
            'x': self.rect.left+self.rect.width-BTN_SIZE, 
            'y': self.rect.top
        })
        self.rmv_btn.hover(COLOURS['ts_btn_idle'], COLOURS['ts_btn_hvr'])
        self.rmv_btn.render(screen)

    def render_tasks(self, screen):
        # render the tasks and desc
        x = self.rect.left
        y = self.rect.top+HEADER+MARGIN

        for i in range(len(self.tasks)):
            self.tasks[i].update_pos(x, y)
            self.tasks[i].render(screen)
            y += self.tasks[i].surf.get_height()+MARGIN

    def update_rect(self, rect):
        # update the rect dimensions
        x = rect['x'] if 'x' in rect else self.rect.left
        y = rect['y'] if 'y' in rect else self.rect.top
        w = rect['w'] if 'w' in rect else self.rect.width
        h = rect['h'] if 'h' in rect else self.rect.height

        self.rect = pg.Rect(x, y, w, h)
        self.surf = pg.Surface((w, h))
    
    def click(self, events, screen, pos):
        # check if the add or rmv buttons are clicked
        add = self.add_btn.click(lambda : self.tasks.append(self.add_new_task(screen, pos)), events)
        rmv = self.rmv_btn.click(lambda : True, events)
        return {
            'add': add,
            'rmv': rmv,
        }

    def task_clicks(self, screen, events):
        # check if any of the tasks are clicked
        # edit or delete btn
        for i in range(len(self.tasks)-1, -1, -1):
            self.tasks[i].click_edit_btn(screen, events)
            delete = self.tasks[i].click_delete_btn(events)
            if delete:
                self.tasks[i:i+1] = []

    def check_holding_task(self):
        # check if the user is trying to begin dragging a task
        for i in range(len(self.tasks)):
            if self.tasks[i].hover():
                return {
                    'taskset': self,
                    'task': i,
                }
        return False
    
    def drag(self, index):
        # update the position of the task by dragging
        self.tasks[index].drag()

    def drop(self, index):
        # let go of the task; no longer dragging task
        self.tasks[index].drop()

    def get_task(self, index):
        # get the task at index
        return self.tasks[index]

    def hover(self):
        # check if the mouse is hovering over the taskset rect
        x, y = pg.mouse.get_pos()
        return self.rect.collidepoint(x, y)
    
    def drop_here(self, task):
        # drop the task here; add the task to the list of tasks
        self.tasks.append(task)

    def add_new_task(self, screen, pos):
        # create a new task
        task_desc = Input('Task Description').run(screen)
        x = pos[0]
        y = pos[1]+50
        for i in range(len(self.tasks)):
            y+=self.tasks[i].surf.get_height()+MARGIN
        return Task(task_desc, self.w, 0, 0)

    def remove_task(self, index):
        # delete this task
        self.tasks[index:index+1] = []

