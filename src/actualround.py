import pygame as pg
import notes
import keyfields

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

