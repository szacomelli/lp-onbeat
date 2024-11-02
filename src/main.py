import pygame as pg
from threading import Timer as tm

pg.init()

class ActualRound:
    def __init__(self, key_fields, notes, interval):
        self.key_fields = key_fields
        self.notes_to_play = notes
        self.notes_interval = interval
        self.notes_played = []
        self.total_points = 0
        self.combo = 1
        self.combo_txt = self.create_text("Combo: ",0)
        self.score_txt = self.create_text("Score: ", 0)

    def play_notes(self):
        while len(self.notes_interval) != 0 and pg.time.get_ticks() >= self.notes_interval[0]:
            if len(self.notes_to_play) != 0:
                self.notes_played.append(self.notes_to_play[0])
                self.notes_to_play.pop(0)
            self.notes_interval.pop(0)

    def draw_objects(self, keys, screen):
        for key in self.key_fields:
            self.combo = key.on_key_press(keys, self.notes_played, self.combo)        
            key.draw_rect(screen)

        for note in self.notes_played:
            note.draw_rect(screen)
        
        screen.blit(self.combo_txt, (500,0))
        screen.blit(self.score_txt, (500,50))

    def update(self, keys):

        for note in self.notes_played:
            note.update()
            if note.destructed:
                self.combo = 1

        total_points = 0
        for key in self.key_fields:
            key.update(keys)
            total_points += key.points

        if total_points < 0: total_points = 0

        self.total_points = total_points
        self.combo_txt = self.create_text("Combo: ",self.combo)
        self.score_txt = self.create_text("Score: ",self.total_points)
        
    def create_text(self, text, number):
        font = pg.font.SysFont('Comic Sans MS', 30)
        return font.render(text+str(number), False, (220, 0, 0))


class KeyField:
    def __init__(self, x, y, unpressed_color, pressed_color, key, mult_scores):
        self.rect = pg.Rect(x, y, 30, 10)
        self.unpressed_color = unpressed_color
        self.pressed_color = pressed_color
        self.key = key
        self.pressed = False
        self.points = 0
        self.combo = 0
        self.last_tick = 0
        self.combo_multiplier_scores = mult_scores

    def draw_rect(self, display):
        if self.pressed == True:
            pg.draw.rect(display, self.pressed_color, self.rect)
        else:
            pg.draw.rect(display, self.unpressed_color, self.rect)

    def on_key_press(self, keys, notes, combo : int):
        if keys[self.key] and not self.pressed:
            note_idx = self.rect.collidelist(notes)
            
            if note_idx != -1:
                actual_note = notes[note_idx]
                if actual_note.note_ended():  self.pressed = True
                self.points += actual_note.calculate_points(*actual_note.points_args)*self.calculate_combo_multiplier()
                
                if actual_note.note_ended():
                    notes[note_idx].updating = False
                    notes.pop(note_idx)

                    if self.detect_FakeNote(actual_note): return 1
                    
                is_SlowNote = isinstance(actual_note, SlowNote)
                actual_tick = pg.time.get_ticks()

                return self.detect_SlowNote(actual_note, is_SlowNote, actual_tick, combo)

            else:
                self.pressed = True
                return 1
        return combo
    
    def calculate_combo_multiplier(self):
        if self.combo >= self.combo_multiplier_scores[0] and self.combo < self.combo_multiplier_scores[1]: return 1
        elif self.combo >= self.combo_multiplier_scores[1] and self.combo < self.combo_multiplier_scores[2]: return 2
        elif self.combo >= self.combo_multiplier_scores[2] and self.combo < self.combo_multiplier_scores[3]: return 3
        elif self.combo >= self.combo_multiplier_scores[3]: return 4

    def detect_FakeNote(self, note):
        if isinstance(note, FakeNote): return True
        else: return False

    def detect_SlowNote(self, note, is_SlowNote, actual_tick, combo):
        if is_SlowNote:
            if note.calculate_delay_end(actual_tick, self.last_tick): 
                self.last_tick = actual_tick
                return combo + 1
            else: return combo
        else: return combo + 1
        
    def update(self, keys):
        if not keys[self.key]:
            self.pressed = False

class Note: 
    def __init__(self, field : KeyField, speed=5, intervals=[[0, 10, 20], [5, 3, 1]]):
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
    def __init__(self, field : KeyField, speed=5, intervals=[[0, 10, 20], [5, 3, 1]]):
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
    def __init__(self, field : KeyField, speed=5,intervals=[[0, 10, 20], [5, 3, 1]], height=150):
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
        self.time_held += 1
        print(self.time_held, self.ticks_per_third)

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
    def __init__(self, field : KeyField, speed=5, intervals=[[0, 10, 20], [5, 3, 1]]):
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

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pg.time.Clock()

key_fields = [KeyField(100, 400, (255, 0, 0), (220, 0, 0), pg.K_a, [0, 1, 2, 5]),
              KeyField(200, 400, (0, 255, 0), (0, 220, 0), pg.K_s, [0, 1, 2, 5]), 
              KeyField(300, 400, (0, 0, 255), (0, 0, 220), pg.K_d, [0, 1, 2, 5]), 
              KeyField(400, 400, (255, 255, 0), (220, 220, 0), pg.K_f, [0, 1, 2, 5])]

notes = [FastNote(key_fields[0]), FastNote(key_fields[1]), FastNote(key_fields[1]), FastNote(key_fields[2]), FastNote(key_fields[3])]
intervals = [0, 0, 500, 0, 1000]

round = ActualRound(key_fields, notes, intervals)
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    round.play_notes()

    screen.fill((0, 0, 0))  # clears the screen
    
    keys = pg.key.get_pressed()
    undone = False
    round.draw_objects(keys, screen)

    round.update(keys)

    pg.display.flip()  # updates the screen
    clock.tick(30)

pg.quit()