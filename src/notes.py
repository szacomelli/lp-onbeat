import pygame as pg
import keyfields as kf
from abc import ABC, abstractmethod
from pathlib import Path
import os


class Note(ABC): 
    def __init__(self, field : kf.KeyField, speed=2, intervals=[[0, 10, 20], [5, 3, 1]]):
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
    def draw(self):
        raise NotImplementedError("You should implement this method")
    
    @abstractmethod
    def update(self):
        raise NotImplementedError("You should implement this method")
    
    @abstractmethod
    def calculate_points(self):
        raise NotImplementedError("You should implement this method")
    
    @abstractmethod
    def note_ended(self):
        raise NotImplementedError("You should implement this method")
    
    def calculate_time_gap(self):
        return self.time_interval - pg.mixer.music.get_pos() 
    
class FastNote(Note):
    def __init__(self, field : kf.KeyField, id, speed=1, intervals=[[0, 10, 20], [5, 3, 1]]):
        super().__init__(field, speed, intervals)
        size = self.field.rect.width*(1-1/6)
        self.y_spawn = 0 - size
        self.rect = pg.Rect(field.rect.centerx - size/2, self.y_spawn, size, size)
        self.points_args = [field.rect.y]

        sprite_path = kf.MakeSprite.load_sprites("./assets/notes/fastnotes/")[id]
        self.sprite = kf.MakeSprite(self.rect, sprite_path)

    def draw(self, display):
        if self.destructed == False:
            # Adicionando o desenho da sprite
            # pg.draw.rect(display, self.color, self.rect)
            self.sprite.draw(display)

    def update(self,speed):
        if self.updating:
            self.rect.centerx = self.field.rect.centerx
            self.rect.width, self.rect.height = self.calculate_size()

            self.rect.y = self.field.rect.y - (self.calculate_time_gap())/speed#+= self.speed
            
            if self.field.rect.bottom + 10 < self.rect.top:
                self.destructed = True
                self.updating = False

    def calculate_points(self):
        bias = self.field.rect.y - self.rect.y
        if bias <= self.point_intervals[0][0] and bias >= -self.point_intervals[0][0]: return self.point_intervals[1][0]
        elif bias <= self.point_intervals[0][1] and bias >= -self.point_intervals[0][1]: return self.point_intervals[1][1]
        elif bias <= self.point_intervals[0][2] and bias >= -self.point_intervals[0][2]: return self.point_intervals[1][2]
        else: return 1

    def calculate_size(self):
        return (self.field.rect.width,self.field.rect.height)

    def note_ended(self):
        return True

class SlowNote(Note):
    def __init__(self, field : kf.KeyField, id, speed=1,intervals=[[0, 10, 20], [5, 3, 1]], height=150):
        super().__init__(field, speed, intervals)
        self.height = height
        width = self.field.rect.width*(1-1/6)
        self.height_ratio = height/width
        
        self.y_spawn = 0 - height
        self.rect = pg.Rect(field.rect.centerx - width/2, self.y_spawn, width, height)

        self.pressed = False
        self.y_holding_start = 0
        self.y_holding_end = 0
        
        self.sprite_sections = []
        num_sprites = int(self.height_ratio)
        self.sprite_heigth = self.height / num_sprites
        filepath = "./assets/notes/slownotes/"

        folders = sorted([folder for folder in os.listdir(filepath) if os.path.isdir(os.path.join(filepath, folder))])
        if not (0 <= id < len(folders)):
            raise ValueError(f"The 'id={id}' index is out of the valid range (0 to {len(folders) - 1}).")
        sprite_folder = os.path.join(filepath, folders[id])
        sprite_files = sorted([file for file in os.listdir(sprite_folder) if os.path.isfile(os.path.join(sprite_folder, file))])
        sprite_dict = {0: 3, num_sprites - 1: 0, num_sprites // 2: 2}

        for i in range(num_sprites):
            sprite_rect = pg.Rect(self.rect.x, self.rect.y + i * self.sprite_heigth, width, self.sprite_heigth)
            sprite_path = os.path.join(sprite_folder, sprite_files[sprite_dict.get(i, 1)])
            self.sprite_sections.append(kf.MakeSprite(sprite_rect, sprite_path))

    def draw(self, display):
        if self.destructed == False:
            # Adicionando desenho da sprite
            # pg.draw.rect(display, self.color, self.rect)
            for sprite in self.sprite_sections:
                sprite.draw(display)

    def update(self, speed):
        if self.updating:
            self.rect.centerx = self.field.rect.centerx
            self.rect.width, self.rect.height = self.calculate_size()

            self.rect.bottom = self.field.rect.y - (self.calculate_time_gap())/speed 

            sprite_height = self.rect.height / len(self.sprite_sections)
            for i, sprite in enumerate(self.sprite_sections):
                sprite.rect.x = self.rect.x
                sprite.rect.y = self.rect.y + i * sprite_height
                sprite.rect.width = self.rect.width
                sprite.rect.height = sprite_height
            
            # if self.field.rect.bottom + 50*self.ratio < self.rect.top and not self.pressed:
            #     self.destructed = True
            #     self.updating = False
                
    def calculate_points(self):
        if self.y_holding_end - self.y_holding_start + 10 > self.rect.height : return 5
        else: return 0

    def calculate_size(self):
        return (self.field.rect.width,self.field.rect.width*self.height_ratio)
    
    def note_ended(self):
        
        if self.rect.top + self.ratio*10 >= self.field.rect.bottom:
            self.y_holding_end = self.rect.y
            return True
        else:
            return False

class FakeNote(Note):
    def __init__(self, field : kf.KeyField, id, speed=2, intervals=[[0, 10, 20], [5, 3, 1]]):
        super().__init__(field, speed, intervals)
        height = self.field.rect.width - self.field.bias
        self.y_spawn = 0 - height
        self.rect = pg.Rect(field.rect.x + 5, self.y_spawn, 20, height)
        self.color = tuple(element/2 for element in self.field.unpressed_color)

        sprite_path = kf.MakeSprite.load_sprites("./assets/notes/fakenotes/")[id]
        self.sprite = kf.MakeSprite(self.rect, sprite_path)
        

    def draw(self, display):
        if self.destructed == False:
            # Adicionando desenho da sprite
            # pg.draw.rect(display, self.color, self.rect)
            self.sprite.draw(display)
            

    def update(self,speed):
        if self.updating:
            self.rect.centerx = self.field.rect.centerx
            self.rect.width, self.rect.height = self.calculate_size()

            self.rect.y = self.field.rect.y - (self.calculate_time_gap())/speed

            if self.field.rect.bottom + 10 < self.rect.top:
                self.destructed = True
                self.field.points += 1
                self.updating = False

    def calculate_points(self):
        return -1
    
    def calculate_size(self):
        return (self.field.rect.width,self.field.rect.height)
    
    def note_ended(self):
        return True
