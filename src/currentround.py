import pygame as pg
import notes
import music
import keyfields
import playground

class CurrentRound:
    def __init__(self, key_fields : keyfields.KeyField, music : music.Music, playground : playground.Playground, screen_size=[480,640],speed=3):
        self.playground = playground
        self.screen_size = screen_size
        self.key_fields = key_fields
        self.notes_to_play = music.notes_list
        self.notes_interval = music.time_intervals
        self.music = music
        self.notes_played = []
        self.total_points = 0
        self.combo_mult_scores = [0, music.total_notes*0.05, music.total_notes*0.1, music.total_notes*0.3]
        self.combo = 0
        self.combo_txt = self.create_text("Combo: ",0)
        self.score_txt = self.create_text("Score: ", 0)
        self.speed = speed

    def start_round(self):
        pg.mixer.music.load(self.music.file_path)
        pg.mixer.music.play()

    def play_notes(self):
        while len(self.notes_interval) != 0 and pg.time.get_ticks() + self.screen_size[0]*self.speed>= self.notes_interval[0]:
            if len(self.notes_to_play) != 0:
                self.notes_to_play[0].time_interval = self.notes_interval[0]
                self.notes_played.append(self.notes_to_play[0])
                self.notes_to_play.pop(0)
            self.notes_interval.pop(0)

    def draw_objects(self, screen : pg.Surface, keys):
        for key in self.key_fields:
            self.on_key_press(keys, self.notes_played)
            key.draw_rect(screen)

        for note in self.notes_played:
            note.draw_rect(screen)
        
        screen.blit(self.combo_txt, (screen.get_width() - 150,0))
        screen.blit(self.score_txt, (screen.get_width() - 150,50))

    def on_key_press(self, keys, notes_list):
        for key_field in self.playground.key_fields:
            if keys[key_field.key] and not key_field.pressed:
                note_idx = key_field.rect.collidelist(notes_list)
                
                if note_idx != -1:
                    actual_note = notes_list[note_idx]
                    self.total_points += actual_note.calculate_points()*self.calculate_combo_multiplier(self.combo)

                    if actual_note.note_ended():
                        key_field.pressed = True
                        notes_list[note_idx].updating = False

                        if key_field.detect_FakeNote(actual_note): 
                            self.combo = 0

                    self.combo = key_field.detect_SlowNote(actual_note, self.combo)

                else:
                    key_field.pressed = True
                    self.combo = 0
    
    def calculate_combo_multiplier(self, combo):
        if combo >= self.combo_mult_scores[0] and combo < self.combo_mult_scores[1]: return 1
        elif combo >= self.combo_mult_scores[1] and combo < self.combo_mult_scores[2]: return 2
        elif combo >= self.combo_mult_scores[2] and combo < self.combo_mult_scores[3]: return 3
        elif combo >= self.combo_mult_scores[3]: return 4

    def update(self, keys, screen, resize):
        if resize:
            (self.screen_size, self.speed) = self.playground.update(screen, self.update_ratio, self.speed,self.screen_size)
            
        for note in self.notes_played:
            note.update(self.speed)
            if note.destructed:
                self.combo = 0
                self.total_points -= 1
                self.notes_played.remove(note)
            elif not note.destructed and note.updating == False: #using not note.update wasn't working
                self.notes_played.remove(note)
        
        for key in self.key_fields:
            key.update(keys)

        if self.total_points < 0: self.total_points = 0

        self.combo_txt = self.create_text("Combo: ",self.combo)
        self.score_txt = self.create_text("Score: ",self.total_points)
        return False

    def update_ratio(self,ratio):
        for note in self.notes_to_play:
            note.ratio = ratio
        for note in self.notes_played:
            note.ratio = ratio

    def create_text(self, text, number):
        font = pg.font.SysFont('Comic Sans MS', 30)
        return font.render(text+str(number), False, (220, 0, 0))
    
