import pygame as pg

class KeyField:
    def __init__(self, x, y, unpressed_color, pressed_color, key):
        self.rect = pg.Rect(x, y, 30, 10)
        self.unpressed_color = unpressed_color
        self.pressed_color = pressed_color
        self.key = key
        self.pressed = False
        self.points = 0
        self.combo = 0

    def draw_rect(self, display):
        if self.pressed == True:
            pg.draw.rect(display, self.pressed_color, self.rect)
        else:
            pg.draw.rect(display, self.unpressed_color, self.rect)

    def on_key_press(self, keys, notes, combo):
        if keys[self.key] and not self.pressed:
            note_idx = self.rect.collidelist(notes)

            self.pressed = True
            
            if note_idx != -1:
                self.points += notes[note_idx].calculate_points(self.rect.y)*combo
                notes[note_idx].updating = False
                notes.pop(note_idx)
                return (combo + 1)
            else: return 1
        else: return combo

    def update(self, keys):
        if not keys[self.key]:
            self.pressed = False

class Note: 
    def __init__(self, field : KeyField, speed=5, intervals=[[0, 10, 20], [5, 3, 1]]):
        self.rect = pg.Rect(field.rect.x + 5, -20, 20, 20)        
        self.color = field.unpressed_color
        self.speed = speed
        self.destructed = False
        self.field = field
        self.updating = True
        self.point_intervals = intervals

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



SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pg.time.Clock()

key_fields = [KeyField(100, 400, (255, 0, 0), (220, 0, 0), pg.K_a),
              KeyField(200, 400, (0, 255, 0), (0, 220, 0), pg.K_s), 
              KeyField(300, 400, (0, 0, 255), (0, 0, 220), pg.K_d), 
              KeyField(400, 400, (255, 255, 0), (220, 220, 0), pg.K_f)]

notes = [Note(key_fields[0]), Note(key_fields[1]), Note(key_fields[1]), Note(key_fields[2])]

# NOTE_INTERVAL = pg.USEREVENT

# pg.time.set_timer()
# pg.time.set_timer(NOTE_INTERVAL, 250, 1)

notes_to_draw = []
intervals = [0,0,500, 0]
combo = 1

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    while len(intervals) != 0 and pg.time.get_ticks() >= intervals[0]:
            if len(notes) != 0:
                notes_to_draw.append(notes[0])
                notes.pop(0)
            intervals.pop(0)

    screen.fill((0,0,0))

    keys = pg.key.get_pressed()

    for key in key_fields:
            combo = key.on_key_press(keys, notes_to_draw, combo)        
            key.draw_rect(screen)

    for note in notes_to_draw:
        note.draw_rect(screen)

    for note in notes_to_draw:
            note.update()
    
    total_points = 0
    for key in key_fields:
        key.update(keys)
        total_points += key.points

    print(total_points, combo)
    pg.display.flip()  # Atualiza a tela
    clock.tick(30)

pg.quit()