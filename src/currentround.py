import pygame as pg
import notes
import music
import playground
import devmode
import os

class CurrentRound:
    def __init__(self,  music : music.Music, screen_size=[480,640], switch_key=pg.K_SPACE, dev=False, music_name="Musica2", editing_music=False):
        self.screen_size = screen_size
        self.active_playground = 0
        self.music_start_pos = 0
        self.dev = devmode.DevMode(music_name, active=dev, editing_music=editing_music)

        
        if dev: self.music = self.dev.active_music
        else: self.music = music
        self.speed = self.music.speed
        self.notes_to_play = self.music.notes_list
        self.notes_interval = self.music.time_intervals

        font_path = os.path.join("assets", "8bitoperator.ttf")
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Fonte não encontrada: {font_path}")
        self.font = pg.font.Font(font_path, 20)
        
        self.start_index = 0
        self.stop_index = -1
        self.max_index = len(self.notes_to_play) - 1
        
        self.total_points = 0
        self.combo = 0
        self.combo_mult_scores = [0, self.music.total_notes*0.05, self.music.total_notes*0.1, self.music.total_notes*0.3]
        
        self.text_x = 0
        if self.music.multiplayer_info[0] and self.music.multiplayer_info[1] == 2:
            self.text_x = screen_size[1] - 80
        self.text_y = [0,30]
        self.text_font = 20
        self.combo_txt = self.create_text("Combo: ",0)
        self.score_txt = self.create_text("Score: ", 0)
        self.text_ratio = [1,1]
        self.switch_key = switch_key
        
        self.msg = ["Miss", "Bad","Great!", "Perfect!",""]
        self.i = 4
        self.messages = [self.font.render(self.msg[0], True, (255, 255, 255)),
                         self.font.render(self.msg[1], True, (255, 255, 255)),
                         self.font.render(self.msg[2], True, (255, 255, 255)),
                         self.font.render(self.msg[3], True, (255, 255, 255)),
                         self.font.render(self.msg[4], True, (255, 255, 255))]
        self.x_pos = 0
        self.y_pos = 0
                      
        self.created_intervals = []

    def start_round(self):
        self.music.play_music()

    def on_event(self, event):
        if self.dev.active:
            self.dev.dev_shorts(event, self.notes_to_play, self.max_index, self.stop_index, self.round_callback, self.music_start_pos, self.change_music)        
        if event.type == pg.KEYDOWN:
            if event.key == self.switch_key:
                self.active_playground = (self.active_playground + 1) % len(self.music.playgrounds)
                
    def round_callback(self, music_start_pos, restart_index, decrease_stop_index):
        if restart_index: self.start_index = 0
        self.music_start_pos = music_start_pos

        if decrease_stop_index: self.stop_index -= 1
        
                       
    def play_notes(self):
        if len(self.notes_to_play) == 0: self.stop_index = self.max_index = -1
        if self.stop_index >= len(self.notes_to_play) - 1: 
            self.stop_index = len(self.notes_to_play) - 2
            self.max_index = self.stop_index
        if len(self.notes_to_play) <= self.stop_index: return
        while self.stop_index != self.max_index and pg.mixer.music.get_pos() + self.music_start_pos + (2000/480)*self.screen_size[0] >= self.notes_interval[self.stop_index + 1]:
            self.stop_index += 1
            
            self.notes_to_play[self.stop_index].time_interval = self.notes_interval[self.stop_index]
    
    def draw_objects(self, screen : pg.Surface, keys):        
        
        for playground in self.music.playgrounds:
            playground.draw(screen)
            for key_fields in playground.key_fields:
                key_fields.draw(screen)

        if len(self.notes_to_play) <= self.stop_index: return
        
        for i in range(self.start_index, self.stop_index+1, 1):
            
            self.notes_to_play[i].draw(screen)
            
        if self.dev.active: self.dev.draw_selection(screen, self.notes_to_play, self.music_start_pos, self.stop_index, self.round_callback)

        combo_rect = self.combo_txt.get_rect(topleft=(self.text_x, self.text_y[0]))
        score_rect = self.score_txt.get_rect(topleft=(self.text_x, self.text_y[1]))
        unified_rect = combo_rect.union(score_rect).inflate(25, 25)
        pg.draw.rect(screen, (150, 80, 180), unified_rect)
            
        if self.dev.active: self.dev.draw(screen, self.music_start_pos, self.text_font)
        screen.blit(self.combo_txt, (self.text_x, self.text_y[0]))
        screen.blit(self.score_txt, (self.text_x, self.text_y[1]))
        screen.blit(self.messages[self.i], (self.x_pos, self.y_pos))
        for playground in self.music.playgrounds:
            playground.make_border(screen)
        

    def on_key_press(self, keys, notes_list):        
        for key_field in self.music.playgrounds[self.active_playground].key_fields:
            if keys[key_field.key] and not key_field.pressed:
                note_idx = key_field.rect.collidelist(notes_list)
                
                if note_idx != -1:
                    actual_note = notes_list[note_idx]

                    if actual_note.note_ended():
                        key_field.pressed = True
                        # VERIFY
                        notes_list[note_idx].updating = False
                        
                        if key_field.detect_FakeNote(actual_note): 
                            self.combo = 0

                    self.combo = key_field.detect_SlowNote(actual_note, self.combo)
                    # VERIFY
                    self.points_message(actual_note, key_field)
                    active_pg = self.music.playgrounds[self.active_playground]
                    pg_rect = active_pg.get_rect()  # Adicione um método `get_rect` em `playground` para obter o rect.
                    self.x_pos = pg_rect.x + (pg_rect.width - self.messages[self.i].get_width()) // 2
                    self.y_pos = pg_rect.y + (pg_rect.height - self.messages[self.i].get_height()) // 2
                    n = actual_note.calculate_points()
                    self.total_points += n*self.calculate_combo_multiplier(self.combo)
                    
                else:
                    if self.dev.active: self.dev.create_music(self.music_start_pos, self.music.playgrounds[self.active_playground].key_fields.index(key_field))
                    key_field.pressed = True
                    self.combo = 0

    def points_message(self, actual_note, key_field):
        n = actual_note.calculate_points()
        if n == 0:
            self.i = 4  # Miss
        elif n == 1:
            self.i = 1  # Bad
        elif n == 3:
            self.i = 2  # Great
        elif n == 5:
            self.i = 3  # Perfect
        else:
            self.i = 4  # Default case

        self.x_pos = (self.screen_size[1] - self.messages[self.i].get_width()) // 2
        self.y_pos = (self.screen_size[0] - self.messages[self.i].get_height()) // 2
        
    def change_music(self):
        if self.dev.active:
            self.music_start_pos = 0
            self.music = self.dev.active_music
            self.notes_to_play = self.music.notes_list.copy()
            self.notes_interval = self.music.time_intervals
            self.start_index = 0
            self.stop_index = -1
            self.max_index = len(self.notes_to_play) - 1
            self.total_points = 0
            self.combo = 0
            self.combo_mult_scores = [0, self.music.total_notes*0.05, self.music.total_notes*0.1, self.music.total_notes*0.3]
            
            for note in self.notes_to_play:
                note.rect.y = 0 - 25*(note.rect.height/25)
            
            self.music.play_music()
            
            self.start_round()
    
    def calculate_combo_multiplier(self, combo):
        if combo >= self.combo_mult_scores[0] and combo < self.combo_mult_scores[1]: return 1
        elif combo >= self.combo_mult_scores[1] and combo < self.combo_mult_scores[2]: return 2
        elif combo >= self.combo_mult_scores[2] and combo < self.combo_mult_scores[3]: return 3
        elif combo >= self.combo_mult_scores[3]: return 4

    def update(self, keys, screen, resize):
        speed = self.speed
        size = self.screen_size
        
        if resize:
            for playground in self.music.playgrounds:
                    (self.screen_size, self.speed) = playground.update(screen, self.update_ratio, speed, size)
        if resize:
            self.text_x = self.text_x*self.text_ratio[0]
            self.text_y[0] = self.text_y[0]*self.text_ratio[0]
            self.text_y[1] = self.text_y[1]*self.text_ratio[0]
            self.text_font = int(round(self.text_font*self.text_ratio[0]))
        
        for playground in self.music.playgrounds:
            for key in playground.key_fields:
                key.update(keys)
                self.on_key_press(keys, self.notes_to_play)
        
        if self.start_index != -1:             
            for i in range(self.start_index,self.stop_index+1,1):
                note = self.notes_to_play[i]
                note.update(self.speed, self.music_start_pos, self.music.label_duration)
                if self.dev.active:
                        if self.dev.active_music.paused:
                            note.destructed = False
                            note.updating = True
                        if i > self.dev.max_visible_index and note.rect.y > 0 and note.rect.y < self.notes_to_play[self.dev.max_visible_index].rect.y: 
                            self.dev.max_visible_index = i
                        if i < self.dev.min_visible_index and (note.rect.y < note.field.rect.y) and note.rect.y > self.notes_to_play[self.dev.min_visible_index].rect.y: 
                            self.dev.min_visible_index = i
                if note.destructed:
                    if note.updating:
                        self.combo = 0
                        self.total_points -= 1
                    self.start_index += 1
                    note.reset()        

        if self.music.has_panning:
            self.music.update()

        if self.total_points < 0: self.total_points = 0

        self.combo_txt = self.create_text("Combo: ",self.combo)
        self.score_txt = self.create_text("Score: ",self.total_points)
        return False

    def update_ratio(self,width_ratio,height_ratio):
        note_ratio = max(width_ratio,height_ratio)
        for note in self.notes_to_play:
            note.ratio = note_ratio
        self.text_ratio = [width_ratio,height_ratio]

    def create_text(self, text, number):
        return self.font.render(text + str(number), True, (255, 255, 255))
    
