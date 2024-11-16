import pygame as pg
import notes

class KeyField:
    def __init__(self, x, y, unpressed_color, pressed_color, key, size=30):
        interior_size = size-size*(1/6)
        self.bias = -interior_size + size
        self.rect = pg.Rect(x, y, size, size)
        self.unpressed_color = unpressed_color
        self.pressed_color = pressed_color

        self.key = key
        self.pressed = False

    def draw_rect(self, display):
        if self.pressed == True:
            pg.draw.rect(display, self.pressed_color, self.rect, width=1)
        else:
            pg.draw.rect(display, self.unpressed_color, self.rect, width=int(self.bias/2))

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