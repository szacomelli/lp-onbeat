from pathlib import Path
import pygame as pg
import notes
import os

class KeyField:
    def __init__(self, x: int, y: int, unpressed_color, pressed_color, key: int, sprite_path: str, size: int = 30):
        interior_size = size - size * (1 / 6)
        self.bias = size - interior_size
        self.rect = pg.Rect(x, y, size, size)
        self.unpressed_color = unpressed_color
        self.pressed_color = pressed_color
        
        self.key = key
        self.pressed = False
        self.sprite = MakeSprite(self.rect, sprite_path)
        
    def draw(self, display):
        self.sprite.draw(display)
        
        # if self.pressed == True:
        #     pg.draw.rect(display, self.pressed_color, self.rect, width=1)
        # else:
        #     pg.draw.rect(display, self.unpressed_color, self.rect, width=int(self.bias/2))

    def detect_FakeNote(self, note):
        if isinstance(note, notes.FakeNote): 
            return True
        else: 
            return False

    def detect_SlowNote(self, note, combo):
        if isinstance(note, notes.SlowNote):
            if note.pressed == False: note.y_holding_start = note.rect.y
            note.pressed = True
            if note.y_holding_end - note.y_holding_start + 10 > note.rect.height : return combo + 1
            else: return combo
        else: return combo + 1

    def update(self, keys):
        if not keys[self.key]:
            self.pressed = False

class MakeSprite:
    def __init__(self, rect, sprite_path):
        self.sprite = pg.image.load(sprite_path).convert_alpha()
        self.rect = rect

    @classmethod
    def load_sprites(cls, filepath: str) -> list:
        sprite_paths = []
        for sprite_file in Path(filepath).iterdir():
            if sprite_file.is_file():
                sprite_paths.append(str(sprite_file))  # Adiciona o caminho do arquivo
        return sorted(sprite_paths)
    
    def draw(self, display):
        scaled_sprite = pg.transform.scale(self.sprite, self.rect.size)
        display.blit(scaled_sprite, self.rect.topleft)