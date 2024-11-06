import pygame as pg
import notes

class KeyField:
    def __init__(self, x, y, unpressed_color, pressed_color, key, mult_scores=[0, 0, 0, 0],size=30):
        interior_size = size-size*(1/6)
        self.bias = -interior_size + size
        self.rect = pg.Rect(x, y, size, size)
        #self.interior_rect = pg.Rect((x+self.bias/2),y+self.bias/2, interior_size, interior_size)
        self.unpressed_color = unpressed_color
        self.pressed_color = pressed_color
        self.key = key
        self.pressed = False
        self.points = 0
        self.combo = 0 #unused
        self.last_tick = 0
        self.combo_multiplier_scores = mult_scores
        self.last_note = None

    def draw_rect(self, display):
        if self.pressed == True:
            pg.draw.rect(display, self.pressed_color, self.rect, width=1)
            #pg.draw.rect(display, (0,0,0), self.interior_rect)
            #print(self.interior_rect.x)
        else:
            pg.draw.rect(display, self.unpressed_color, self.rect, width=int(self.bias/2))
            #pg.draw.rect(display, (0,0,0), self.interior_rect)
            #print(self.rect.x,self.interior_rect.x)

    def on_key_press(self, keys, notes_list, combo : int):
        if keys[self.key] and not self.pressed:
            #print(pg.time.get_ticks())
            note_idx = self.rect.collidelist(notes_list)
            
            if note_idx != -1:
                actual_note = notes_list[note_idx]
                if actual_note.note_ended():  self.pressed = True
                self.points += actual_note.calculate_points(*actual_note.points_args)*self.calculate_combo_multiplier(combo)
               # print(actual_note.calculate_points(*actual_note.points_args))
                if actual_note.note_ended():
                    notes_list[note_idx].updating = False
                    notes_list.pop(note_idx)

                    if self.detect_FakeNote(actual_note): 
                        return 0
                    
                is_SlowNote = isinstance(actual_note, notes.SlowNote)
                actual_tick = pg.time.get_ticks()
                return self.detect_SlowNote(actual_note, is_SlowNote, actual_tick, combo)

            else:
                self.pressed = True
                return 0
        return combo
    
    def calculate_combo_multiplier(self, combo):
        if combo >= self.combo_multiplier_scores[0] and combo < self.combo_multiplier_scores[1]: return 1
        elif combo >= self.combo_multiplier_scores[1] and combo < self.combo_multiplier_scores[2]: return 2
        elif combo >= self.combo_multiplier_scores[2] and combo < self.combo_multiplier_scores[3]: return 3
        elif combo >= self.combo_multiplier_scores[3]: return 4

    def detect_FakeNote(self, note):
        if isinstance(note, notes.FakeNote): 
            return True
        else: 
            return False

    def detect_SlowNote(self, note, is_SlowNote, actual_tick, combo):
        if is_SlowNote:
            note.pressed = True
            if note.calculate_delay_end(actual_tick, self.last_tick): 
                self.last_tick = actual_tick
                return combo + 1
            else: 
                return combo
        else: return combo + 1
        
    def update(self, keys):
        if not keys[self.key]:
            self.pressed = False
        if self.points < 0: self.points = 0
