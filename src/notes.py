import pygame as pg
import keyfields
from abc import ABC, abstractmethod

class Note(ABC): 
    def __init__(self, field : keyfields.KeyField, speed=2, intervals=[[5, 10, 30], [5, 3, 1]]):
        self.color = field.unpressed_color
        self.speed = speed
        self.destructed = False
        self.field = field
        self.updating = True
        self.point_intervals = intervals
        self.points_args = []
        self.time_interval = 0
        self.ratio = 1

    @abstractmethod
    def draw_rect(self):
        raise NotImplementedError("You should implement this method")
    
    @abstractmethod
    def update(self):
        raise NotImplementedError("You should implement this method")
    
    @abstractmethod
    def calculate_points(self, speed, starting_pos):
        raise NotImplementedError("You should implement this method")
    
    @abstractmethod
    def note_ended(self):
        raise NotImplementedError("You should implement this method")
    
    def calculate_time_gap(self, starting_pos):
        return self.time_interval - pg.mixer.music.get_pos() - starting_pos
    
    def reset(self):
        self.destructed = False
        self.updating = True
        
    
class FastNote(Note):
    def __init__(self, field : keyfields.KeyField, speed=1, intervals=[[5, 10, 20], [5, 3, 1]]):
        super().__init__(field, speed, intervals)
        size = self.field.rect.width*(1-1/6)
        self.y_spawn = 0 - size
        self.rect = pg.Rect(field.rect.centerx - size/2, self.y_spawn, size, size)
        self.points_args = [field.rect.y] 

    def draw_rect(self, display):
        if self.updating == True and self.destructed == False:
            if abs(self.rect.y - self.field.rect.y) <= 10*self.ratio:
                pg.draw.rect(display, (255,255,255), self.rect)
            else:
                pg.draw.rect(display, self.color, self.rect)

    def update(self, speed, starting_pos, label_duration):
            self.rect.centerx = self.field.rect.centerx
            self.rect.width, self.rect.height = self._calculate_size()
            

            self.rect.y = self.field.rect.y - (self.calculate_time_gap(starting_pos))/speed#+= self.speed
            if self.field.rect.bottom + 10 < self.rect.top:
                self.destructed = True
                

    def calculate_points(self):
        bias = self.field.rect.y - self.rect.y
        if bias <= self.point_intervals[0][0] and bias >= -self.point_intervals[0][0]: return self.point_intervals[1][0]
        elif bias <= self.point_intervals[0][1] and bias >= -self.point_intervals[0][1]: return self.point_intervals[1][1]
        elif bias <= self.point_intervals[0][2] and bias >= -self.point_intervals[0][2]: return self.point_intervals[1][2]
        else: return 1

    def _calculate_size(self):
        return (self.field.rect.width,self.field.rect.height)

    def note_ended(self):
        return True

class SlowNote(Note):
    def __init__(self, field : keyfields.KeyField, speed=1,intervals=[[5, 10, 30], [5, 3, 1]], height=150):
        super().__init__(field, speed, intervals)
        self.height = height
        width = self.field.rect.width*(1-1/6)
        self.height_ratio = height/width
        
        self.y_spawn = 0 - height
        self.rect = pg.Rect(field.rect.centerx - width/2, self.y_spawn, width, height)

        self.pressed = False
        self.y_holding_start = 0
        self.y_holding_end = 0
        
        self.top_selected = False
        self.first_update = True

    def draw_rect(self, display):
        if self.updating == True:# and self.destructed == False:
            pg.draw.rect(display, self.color, self.rect)

    def update(self, speed, starting_pos, label_duration):
        self.rect.height = (int((self.rect.height*self.speed)/label_duration))*label_duration/self.speed + self.rect.width
        self.height_ratio = self.rect.height/self.rect.width
        self.speed = speed
        self.rect.centerx = self.field.rect.centerx
        self.rect.width, self.rect.height = self._calculate_size()
        self.rect.bottom = self.field.rect.bottom- (self.calculate_time_gap(starting_pos))/speed 
        
        if self.field.rect.bottom + 50*self.ratio < self.rect.top:# and not self.pressed:
            self.pressed = False
            self.destructed = True
                
    def calculate_points(self):
        if self.y_holding_end - self.y_holding_start + 10*self.ratio > self.rect.height : 
            return 5
        else: return 0

    def reset(self):
        self.destructed = False
        self.updating = True
        self.pressed = False
        self.y_holding_start = 0
        self.y_holding_end = 0

    def _calculate_size(self):
        return (self.field.rect.width,self.field.rect.width*self.height_ratio)
    
    def note_ended(self):
        
        if self.rect.top + self.ratio*10 >= self.field.rect.bottom:
            self.y_holding_end = self.rect.y
            return True
        else:
            return False

class FakeNote(Note):
    def __init__(self, field : keyfields.KeyField, speed=2, intervals=[[0, 10, 20], [5, 3, 1]]):
        super().__init__(field, speed, intervals)
        height = self.field.rect.width - self.field.bias
        self.y_spawn = 0 - height
        self.rect = pg.Rect(field.rect.x + 5, self.y_spawn, 20, height)
        self.color = tuple(element/2 for element in self.field.unpressed_color)
        

    def draw_rect(self, display):
        if self.destructed == False:
            pg.draw.rect(display, self.color, self.rect)

    def update(self,speed, starting_pos, label_duration):
        if self.updating:
            self.rect.centerx = self.field.rect.centerx
            self.rect.width, self.rect.height = self._calculate_size()

            self.rect.y = self.field.rect.y - (self.calculate_time_gap(starting_pos))/speed

            if self.field.rect.bottom + 10 < self.rect.top:
                self.destructed = True
                #self.field.points += 1
                self.updating = False
                
                

    def calculate_points(self):
        return -1
    
    def _calculate_size(self):
        return (self.field.rect.width,self.field.rect.height)
    
    def note_ended(self):
        return True
