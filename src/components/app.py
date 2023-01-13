import pygame as pg
from src.settings import FPS, MARGIN, PAD, FONT
from src.components.button import Button
from src.components.taskset import TaskSet
from src.components.task import Task
from src.components.input import Input
from src.components.colour_input import ColourInput

class App:
    def __init__(self, data, screen, clock):
        self.tasksets = []
        self.clock = clock
        self.screen = screen
        self.new_taskset_btn = Button(3*self.screen.get_width()/4, 
                            0, 
                            2*PAD+FONT.text_width('Add New Taskset', 12), 
                            50, 
                            'Add New Taskset')
        self.currently_dragging = None

        self.import_data(data)
    
    def run(self):

        while True:

            events = pg.event.get()

            for event in events:
                if event.type == pg.QUIT:
                    return self.save_data()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return self.save_data()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.begin_drag()
                if event.type == pg.MOUSEBUTTONUP:
                    self.drop()

            self.click(events)
            self.allow_drag()

            self.screen.fill((0, 0, 0))
            self.render()
            
            self.clock.tick(FPS)
            pg.display.update()
    
    #######
    # RENDERING
    #######
    def render(self):
        # draw the top bar
        self.render_bar()

        # draw the tasksets
        self.render_tasksets()
    
    def render_bar(self):
        # bar
        pg.draw.rect(self.screen, (255, 255, 255), (0, 0, self.screen.get_width(), 50))

        # button
        self.new_taskset_btn.hover((255, 0, 0), (0, 255, 0))
        self.new_taskset_btn.render(self.screen)

    def render_tasksets(self):
        x = MARGIN
        for taskset in self.tasksets:
            taskset.update_rect({
                'x': x,
            })
            x+=taskset.rect.w+MARGIN
            taskset.render(self.screen)
            taskset.render_tasks(self.screen)

        # render currently dragging task
        if self.currently_dragging:
            self.currently_dragging['taskset'].tasks[self.currently_dragging['task']].render(self.screen)
    #######
    # BUTTON EVENTS
    #######
    def click(self, events):
        self.new_taskset_btn.click(lambda : self.tasksets.append(self.new_taskset(Input('Taskset Name').run(self.screen), 
                                                                                  ColourInput('Taskset Colour').run(self.screen))), 
                                    events)
        taskset_to_remove = None
        for i in range(len(self.tasksets)):
            click = None
            self.tasksets[i].task_clicks(self.screen, events)
            if i==0:
                click = self.tasksets[i].click(events, self.screen, (MARGIN, 100))
            else:
                click = self.tasksets[i].click(events, self.screen, (i*(self.tasksets[i-1].w+MARGIN)+MARGIN, 100))
            
            if click['rmv']:
                taskset_to_remove = self.tasksets[i]
            
        if taskset_to_remove:
            self.tasksets.remove(taskset_to_remove)

    #######
    # DRAGGING TASKS
    #######
    def allow_drag(self):
        if self.currently_dragging:
            self.currently_dragging['taskset'].drag(self.currently_dragging['task'])

    def begin_drag(self):
        for taskset in self.tasksets:
            self.currently_dragging = taskset.check_holding_task()
            if self.currently_dragging:
                return
    
    def drop(self):
        if self.currently_dragging:
            dragged_task = None
            dragged_task = self.currently_dragging['taskset'].get_task(self.currently_dragging['task'])
            self.currently_dragging['taskset'].drop(self.currently_dragging['task'])
            
            dropped = False
            for taskset in self.tasksets:
                if taskset.hover():
                    if taskset == self.currently_dragging['taskset']:
                        break
                    taskset.drop_here(dragged_task)
                    dropped = True
                    
            if dropped:
                self.currently_dragging['taskset'].remove_task(self.currently_dragging['task'])
            
            self.currently_dragging = False
    
    #######
    # NEW TASKSET
    #######
    def new_taskset(self, name, c):
        x = MARGIN
        for taskset in self.tasksets:
            x+=taskset.w+MARGIN
        return TaskSet(c, name, [], x, 100)

    #######
    # SAVING AND IMPORTING DATA
    #######
    def save_data(self):
        data = {}
        for taskset in self.tasksets:
            data[taskset.name] = {
                'c': taskset.c,
                'tasks': list(map(lambda task : task.desc, taskset.tasks)),
            }
        
        return data

    def import_data(self, data):
        for j, key in enumerate(data.keys()):
            taskset_data = data[key]
            tasks = []
            for i in range(len(taskset_data['tasks'])):
                if j==0:
                    tasks.append(Task(taskset_data['tasks'][i], 300, MARGIN, 100))
                else:
                    tasks.append(Task(taskset_data['tasks'][i], 300, j*(self.tasksets[j-1].w+MARGIN)+MARGIN, 100))
            if j==0:
                self.tasksets.append(TaskSet(taskset_data['c'], key, tasks, MARGIN, 100))
            else:
                self.tasksets.append(TaskSet(taskset_data['c'], key, tasks, j*(self.tasksets[j-1].w+MARGIN)+MARGIN, 100))