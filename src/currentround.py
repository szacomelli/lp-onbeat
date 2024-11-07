import pygame as pg
import notes
import music
import keyfields

class CurrentRound:
    def __init__(self, key_fields : keyfields.KeyField, music : music.Music, playground, screen_size=[480,640],speed=3):
        self.playground = playground
        self.screen_size = screen_size
        self.key_fields = key_fields
        self.notes_to_play = music.notes_list
        self.notes_interval = music.time_intervals
        self.music = music
        for key_field in self.key_fields:
            key_field.combo_multiplier_scores = [0, music.total_notes*0.05, music.total_notes*0.1, music.total_notes*0.3]
        self.notes_played = []
        self.total_points = 0
        self.combo = 0
        self.combo_txt = self.create_text("Combo: ",0)
        self.score_txt = self.create_text("Score: ", 0)
        self.speed = speed

    def start_round(self):
        pg.mixer.music.load(self.music.file_path)
        pg.mixer.music.play()
        self.music.update_intervals()

    def play_notes(self):
        while len(self.notes_interval) != 0 and pg.time.get_ticks() + self.screen_size[0]*self.speed>= self.notes_interval[0]:
            if len(self.notes_to_play) != 0:
                self.notes_to_play[0].time_interval = self.notes_interval[0]
                self.notes_played.append(self.notes_to_play[0])
                self.notes_to_play.pop(0)
            self.notes_interval.pop(0)

    def draw_objects(self, keys, screen : pg.Surface):
        for key in self.key_fields:
            self.combo = key.on_key_press(keys, self.notes_played, self.combo) 
            key.draw_rect(screen)

        for note in self.notes_played:
            note.draw_rect(screen)
        
        screen.blit(self.combo_txt, (screen.get_width() - 150,0))
        screen.blit(self.score_txt, (screen.get_width() - 150,50))

    def update(self, keys, screen, resize):
        if resize:
            (self.screen_size, self.speed) = self.playground.update(screen, self.notes_played,self.speed,self.screen_size)
            
        for note in self.notes_played:
            note.update(self.speed)
            if note.destructed:
                self.combo = 0
                self.notes_played.remove(note)

        total_points = 0
        for key in self.key_fields:
            key.update(keys)
            total_points += key.points

        if total_points < 0: total_points = 0

        self.total_points = total_points
        self.combo_txt = self.create_text("Combo: ",self.combo)
        self.score_txt = self.create_text("Score: ",self.total_points)
        return False

    def create_text(self, text, number):
        font = pg.font.SysFont('Comic Sans MS', 30)
        return font.render(text+str(number), False, (220, 0, 0))
    
    def SlowKey_held_reset(self, key):
        # this prevents the player of exploiting SlowNotes.calculate_points by 
        # spamming the button instead of holding it 
        for key_field in self.key_fields:
            if key == key_field.key:
                for note in self.notes_played:
                    if isinstance(note, notes.SlowNote) and note.field == key_field:
                        note.time_held = 0

