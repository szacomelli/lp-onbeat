import pygame as pg
import notes
import music
import keyfields
import playground

class CurrentRound:
    def __init__(self,  music : music.Music,  screen_size=[480,640], switch_key=pg.K_SPACE):
        self.screen_size = screen_size
        self.active_playground = 0
        
        self.music = music
        self.speed = music.speed
        self.notes_to_play = music.notes_list
        self.notes_interval = music.time_intervals
        self.notes_played = []
        
        self.total_points = 0
        self.combo = 0
        self.combo_mult_scores = [0, music.total_notes*0.05, music.total_notes*0.1, music.total_notes*0.3]
        
        self.text_x = 0
        if music.multiplayer_info[0] and self.music.multiplayer_info[1] == 2:
            self.text_x = screen_size[1] - 80
        self.text_y = [0,30]
        self.text_font = 20
        self.combo_txt = self.create_text("Combo: ",0)
        self.score_txt = self.create_text("Score: ", 0)
        self.text_ratio = [1,1]
        self.switch_key = switch_key

    def start_round(self):
        self.music.play_music()

    def on_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == self.switch_key:
                self.active_playground = (self.active_playground + 1) % len(self.music.playgrounds)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LSHIFT:
                pg.mixer.music.pause()
                self.music.channel.pause()
        if event.type == pg.KEYUP:
            if event.key == pg.K_LSHIFT:
                pg.mixer.music.unpause()
                self.music.channel.unpause()
                
    def play_notes(self):
        while len(self.notes_interval) != 0 and pg.time.get_ticks() + self.screen_size[0]*self.speed>= self.notes_interval[0]:
            if len(self.notes_to_play) != 0:
                self.notes_to_play[0].time_interval = self.notes_interval[0]
                self.notes_played.append(self.notes_to_play[0])
                self.notes_to_play.pop(0)
            self.notes_interval.pop(0)

    def draw_objects(self, screen : pg.Surface, keys):
        abba = keyfields.MakeSprite.make_background(screen,"./assets/game_screen/barras.png", 100, 300)
        abba.draw(screen)
        
        for playground in self.music.playgrounds:
            for key_fields in playground.key_fields:
                # self.on_key_press(keys, self.notes_played)
                key_fields.draw(screen)
        

        for note in self.notes_played:
            note.draw(screen)
        
        screen.blit(self.combo_txt, (self.text_x, self.text_y[0]))
        screen.blit(self.score_txt, (self.text_x, self.text_y[1]))

    def on_key_press(self, keys, notes_list):
        for key_field in self.music.playgrounds[self.active_playground].key_fields:
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
        speed = self.speed
        size = self.screen_size

        # verify
        for playground in self.music.playgrounds:
            if resize:
                (self.screen_size, self.speed) = playground.update(screen, self.update_ratio, speed, size)
        if resize:
            self.text_x = self.text_x*self.text_ratio[0]
            self.text_y[0] = self.text_y[0]*self.text_ratio[0]
            self.text_y[1] = self.text_y[1]*self.text_ratio[0]
            self.text_font = int(round(self.text_font*self.text_ratio[0]))
        
        for playground in self.music.playgrounds:
            for key in playground.key_fields:
                key.update(keys)
                self.on_key_press(keys, self.notes_played)
        
        for note in self.notes_played:
            note.update(self.speed)
            if note.destructed:
                self.combo = 0
                self.total_points -= 1
                self.notes_played.remove(note)
            elif not note.destructed and note.updating == False: #using not note.update wasn't working
                self.notes_played.remove(note)
        
        
        # if self.active_playground == 1:
        #     self.music.channel.set_volume(0,1)
        # else:
        #     self.music.channel.set_volume(1,0)
        if self.total_points < 0: self.total_points = 0

        self.combo_txt = self.create_text("Combo: ",self.combo)
        self.score_txt = self.create_text("Score: ",self.total_points)
        return False

    def update_ratio(self,width_ratio,height_ratio):
        note_ratio = max(width_ratio,height_ratio)
        for note in self.notes_to_play:
            note.ratio = note_ratio
        for note in self.notes_played:
            note.ratio = note_ratio
        self.text_ratio = [width_ratio,height_ratio]

    def create_text(self, text, number):
        font = pg.font.SysFont('Comic Sans MS', self.text_font)
        return font.render(text+str(number), False, (220, 0, 0))
    