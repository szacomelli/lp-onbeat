import pygame as pg
import notes
import music
import keyfields
import playground
import devmode

class CurrentRound:
    def __init__(self,  music : music.Music, screen_size=[480,640], switch_key=pg.K_SPACE, dev=False):
        # basic atributtes
        self._screen_size = screen_size
        self.active_playground = 0
        self.music_start_pos = 0
        self.__dev_active = dev
        
        # change the music to dev-selected one. maybe it's better to modularize the dev class to call round, not the other way around
        # also defines some basic attributes for the music and notes
        self.music = music
        self.speed = self.music.speed
        self.notes_to_play = self.music.notes_list
        self.notes_interval = self.music.time_intervals
        self.start_index = 0
        self.stop_index = -1
        self.max_index = len(self.notes_to_play) - 1
        
        # score attributes
        self.total_points = 0
        self.combo = 0
        self._combo_mult_scores = [0, self.music.total_notes*0.05, self.music.total_notes*0.1, self.music.total_notes*0.3]
        self._remaining_misses = int(len(self.notes_to_play)*0.15)
        self.game_over = False
        
        self.text_x = 0
        if self.music.multiplayer_info[0] and self.music.multiplayer_info[1] == 2:
            self.text_x = screen_size[1] - 80
        self.text_y = [0,30]
        self.text_font = 20
        self._combo_txt = self.create_text("Combo: ",0)
        self._score_txt = self.create_text("Score: ", 0)
        self.text_ratio = [1,1]
        self.__switch_key = switch_key
        
    # starts the music
    def start_round(self):
        self.music.play_music()

    # keep track of pressed keys; it's used just for the Stakes level or for dev
    def on_event(self, event):
        # if self.dev.active:
        #     self.dev.dev_shorts(event, self.notes_to_play, self.max_index, self.stop_index, self.round_callback, self.music_start_pos, self.change_music)        
        if event.type == pg.KEYDOWN:
            if event.key == self.__switch_key:
                self.active_playground = (self.active_playground + 1) % len(self.music.playgrounds)
        
    # selects notes that need to be placed in screen               
    def play_notes(self):
        if len(self.notes_to_play) == 0: self.stop_index = self.max_index = -1
        if self.stop_index >= len(self.notes_to_play) - 1: 
            self.stop_index = len(self.notes_to_play) - 2
            self.max_index = self.stop_index
        
        while self.stop_index != self.max_index and pg.mixer.music.get_pos() + self.music_start_pos + (2000/480)*self._screen_size[0] >= self.notes_interval[self.stop_index + 1]:
            self.stop_index += 1
            
            self.notes_to_play[self.stop_index].time_interval = self.notes_interval[self.stop_index]
    
    # draw all needed objects
    def draw_objects(self, screen : pg.Surface, keys):
        for playground in self.music.playgrounds:
            for key_fields in playground.key_fields:
                key_fields.draw_rect(screen)

        if len(self.notes_to_play) <= self.stop_index: return
        
        for i in range(self.start_index, self.stop_index+1, 1):
            
            self.notes_to_play[i].draw_rect(screen)
        
        screen.blit(self._combo_txt, (self.text_x, self.text_y[0]))
        screen.blit(self._score_txt, (self.text_x, self.text_y[1]))
        

    # keep track of key_fields pressed
    def on_key_press(self, keys, notes_list, dev=None):        
        for key_field in self.music.playgrounds[self.active_playground].key_fields:
            if keys[key_field.key] and not key_field.pressed:
                note_idx = key_field.rect.collidelist(notes_list)
                if note_idx != -1:
                    actual_note = notes_list[note_idx]
                    if actual_note.note_ended():
                        key_field.pressed = True
                        notes_list[note_idx].updating = False
                        if key_field.detect_FakeNote(actual_note): 
                            self.combo = 0
                    self.combo = key_field.detect_SlowNote(actual_note, self.combo)
                    self.total_points += actual_note.calculate_points()*self.calculate_combo_multiplier(self.combo)
                    self._remaining_misses += 1
                else:
                    if self.__dev_active: 
                        dev.create_music(self.music_start_pos, self.music.playgrounds[self.active_playground].key_fields.index(key_field))
                    key_field.pressed = True
                    self.combo = 0
                    self._remaining_misses -= 1
    
    # just calculates the multiplier the player gets by each hit note
    def calculate_combo_multiplier(self, combo):
        if combo >= self._combo_mult_scores[0] and combo < self._combo_mult_scores[1]: return 1
        elif combo >= self._combo_mult_scores[1] and combo < self._combo_mult_scores[2]: return 2
        elif combo >= self._combo_mult_scores[2] and combo < self._combo_mult_scores[3]: return 3
        elif combo >= self._combo_mult_scores[3]: return 4

    # updates all needed objects
    def update(self, keys, screen, resize, dev=None):
        speed = self.speed
        size = self._screen_size
        if resize:
            for playground in self.music.playgrounds:
                    (self._screen_size, self.speed) = playground.update(screen, self.update_ratio, speed, size)
        if resize:
            self.text_x = self.text_x*self.text_ratio[0]
            self.text_y[0] = self.text_y[0]*self.text_ratio[0]
            self.text_y[1] = self.text_y[1]*self.text_ratio[0]
            self.text_font = int(round(self.text_font*self.text_ratio[0]))
        
        for playground in self.music.playgrounds:
            for key in playground.key_fields:
                key.update(keys)
                self.on_key_press(keys, self.notes_to_play,dev)
        
        if self.start_index != -1:             
            for i in range(self.start_index,self.stop_index+1,1):
                note = self.notes_to_play[i]
                note.update(self.speed, self.music_start_pos, self.music.label_duration)
                if self.__dev_active:
                        if dev.active_music.paused:
                            note.destructed = False
                            note.updating = True
                        if i > dev.max_visible_index and note.rect.y > 0 and note.rect.y < self.notes_to_play[dev.max_visible_index].rect.y: 
                            dev.max_visible_index = i
                        if i < dev.min_visible_index and (note.rect.y < note.field.rect.y) and note.rect.y > self.notes_to_play[dev.min_visible_index].rect.y: 
                            dev.min_visible_index = i

                if note.destructed:
                    hasSlow = False
                    for j in range(0,self.notes_to_play.index(note)):
                        if isinstance(self.notes_to_play[j], notes.SlowNote) and self.notes_to_play[j].destructed == False:
                            hasSlow = True
                    if note.updating:
                        self.combo = 0
                        self._remaining_misses -= 1
                        self.total_points -= 1
                    if not hasSlow: self.start_index += 1
                           

        if self.music.has_panning:
            self.music.update()

        if self.total_points < 0: self.total_points = 0
        if self._remaining_misses <= 0: self.game_over = True
        
        self._combo_txt = self.create_text("Combo: ",self.combo)
        self._score_txt = self.create_text("Score: ",self.total_points)
        return False

    # update the ratio (the ratio is between the current and original screen size)
    def update_ratio(self,width_ratio,height_ratio):
        note_ratio = max(width_ratio,height_ratio)
        for note in self.notes_to_play:
            note.ratio = note_ratio
            for interval in note.point_intervals[0]:
                interval = interval * width_ratio
        self.text_ratio = [width_ratio,height_ratio]

    # create a text, used for score and combo
    def create_text(self, text, number):
        font = pg.font.SysFont('Comic Sans MS', self.text_font)
        return font.render(text+str(number), False, (220, 0, 0))
    
