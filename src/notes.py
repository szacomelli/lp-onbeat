import pygame as pg
import keyfields
class Note: 
    def __init__(self, field : keyfields.KeyField, speed=5, intervals=[[0, 10, 20], [5, 3, 1]]):
        self.color = field.unpressed_color
        self.speed = speed
        self.destructed = False
        self.field = field
        self.updating = True
        self.point_intervals = intervals
        self.points_args = []

    def draw_rect(self):
        raise NotImplementedError("You should implement this method")
    
    def update(self):
        raise NotImplementedError("You should implement this method")
    
    def calculate_points(self):
        raise NotImplementedError("You should implement this method")
    
    def note_ended(self):
        raise NotImplementedError("You should implement this method")
    
class FastNote(Note):
    def __init__(self, field : keyfields.KeyField, speed=5, intervals=[[0, 10, 20], [5, 3, 1]]):
        super().__init__(field, speed, intervals)
        height = 20
        self.rect = pg.Rect(field.rect.x + 5, 0 - height, 20, height)
        self.points_args = [field.rect.y] 

    def draw_rect(self, display):
        if self.destructed == False:
            pg.draw.rect(display, self.color, self.rect)

    def update(self):
        if self.updating:
            self.rect.y += self.speed
            if self.field.rect.bottom + 10 < self.rect.top:
                self.destructed = True
                self.field.points -= 1
                self.updating = False

    def calculate_points(self, field_y):
        bias = field_y - self.rect.y
        if bias <= self.point_intervals[0][0] and bias >= -self.point_intervals[0][0]: return self.point_intervals[1][0]
        elif bias <= self.point_intervals[0][1] and bias >= -self.point_intervals[0][1]: return self.point_intervals[1][1]
        elif bias <= self.point_intervals[0][2] and bias >= -self.point_intervals[0][2]: return self.point_intervals[1][2]
        else: return 1

    def note_ended(self):
        return True

class SlowNote(Note):
    def __init__(self, field : keyfields.KeyField, speed=5,intervals=[[0, 10, 20], [5, 3, 1]], height=150):
        super().__init__(field, speed, intervals)
        self.rect = pg.Rect(field.rect.x + 5, 0 - height, 20, height)
        self.time_held = 0
        self.ticks_per_third = round(height / (speed*3))

    def draw_rect(self, display):
        if self.destructed == False:
            pg.draw.rect(display, self.color, self.rect)

    def update(self):
        if self.updating:
            self.rect.y += self.speed
            if self.field.rect.bottom + 10 < self.rect.top:
                self.destructed = True
                self.field.points -= 1
                self.updating = False
                
    def calculate_points(self):
        # spamming the button can make this grow too much (bug in the game)
        # fix this creating a module which uses self.field, event.get(), KEY_UP and time_held
        self.time_held += 1
        #debug: print(self.time_held, self.ticks_per_third)

        if self.time_held == self.ticks_per_third:
            return 1
        if self.time_held == 2*self.ticks_per_third:
            return 3
        if self.time_held == 3*self.ticks_per_third:
            return 5
        else: return 0

    def calculate_delay_end(self, actual_tick, last_tick):
        seconds_per_third = self.ticks_per_third*1000/30 # how many seconds it takes to move a third of the note
        if actual_tick > last_tick + seconds_per_third: return True
        else: return False
    
    def note_ended(self):
        if self.rect.y + 5 >= self.field.rect.y:
            return True
        else:
            return False

class FakeNote(Note):
    def __init__(self, field : keyfields.KeyField, speed=5, intervals=[[0, 10, 20], [5, 3, 1]]):
        super().__init__(field, speed, intervals)
        height = 20
        self.rect = pg.Rect(field.rect.x + 5, 0 - height, 20, height)
        self.color = tuple(element/2 for element in self.field.unpressed_color)
        

    def draw_rect(self, display):
        if self.destructed == False:
            pg.draw.rect(display, self.color, self.rect)

    def update(self):
        if self.updating:
            self.rect.y += self.speed
            if self.field.rect.bottom + 10 < self.rect.top:
                self.destructed = True
                self.field.points += 1
                self.updating = False

    def calculate_points(self):
        return -1
    
    def note_ended(self):
        return True
