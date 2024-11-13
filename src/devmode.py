import pygame as pg
import music
import json
import playground as pgr

pg_numbers = [1,1]

playgrounds = [pgr.Playground(50,640,480,keys=[pg.K_d,pg.K_f,pg.K_j,pg.K_k], blank_space_percentage=0.1,pg_numbers=pg_numbers)]


class VoidMusic(music.Music):
    def __init__(self, file, speed):
        self.paused = False
        
        self.file_path = file
        self.notes_list = []
        self.labels = []
        self.columns = []
        self.time_intervals = []
        self.multiplayer_info = [False, 1]
        self.total_notes = 0
        self.speed = speed
        self.playgrounds = playgrounds
        self.song = pg.mixer.Sound(file)
        self.channel = pg.mixer.Channel(1)
        self.has_panning = False
        a = pg.mixer.Sound(self.file_path)
        self.length = a.get_length()

class PlayerMusic(music.Music):
    def __init__(self, file, speed, int_columns, labels, bpm, fake_notes, slow_notes, slow_heights):
        self.paused = False
        
        self.bpm = bpm
        self.columns = int_columns
        self.fake_notes = fake_notes
        self.slow_notes = slow_notes
        self.slow_heights = slow_heights    
        self.playgrounds = playgrounds
        self.multiplayer_info = [False, 1]
        self.file_path = file
        
        self.notes_list = self.create_notes(self.playgrounds)
        self.labels = labels
        self.time_intervals = self.create_intervals()
        
        self.total_notes = len(self.notes_list)
        self.speed = speed
        
        
        self.song = pg.mixer.Sound(file)
        self.channel = pg.mixer.Channel(1)
        self.has_panning = False
        a = pg.mixer.Sound(self.file_path)
        self.length = a.get_length()
        
        
    def create_intervals(self):
        intervals = []
        label_length = 60000/(4*self.bpm)
        for i in self.labels:
            intervals.append(i*label_length)
        return intervals
    
    def create_notes(self, playgrounds : list[pgr.Playground]):
        note_list = self.int_to_notes(playgrounds[0].key_fields,self.columns,self.slow_notes,self.fake_notes,self.slow_heights)
        return note_list

class DevMode:
    
    def __init__(self, music_name, keys=[[pg.K_d,pg.K_f,pg.K_j,pg.K_k]],dkeys=[pg.K_LSHIFT, pg.K_LEFT, pg.K_RIGHT, pg.K_r, pg.K_m], active=False):
        self.configs = self.read_configs()
        self.music = music_name
        self.active = active
        self.developer_keys = dkeys
        self.active_music_idx = 1
        self.hidden_music_idx = 0
        self.BPM = self.configs[self.music]["BPM"]

        if self.active:
            self.music_list = [
                VoidMusic(self.configs[self.music]["music_file"], self.configs[self.music]["speed"]),
                PlayerMusic(self.configs[self.music]["music_file"], self.configs[self.music]["speed"],
                            self.configs[self.music]["keyfields"], self.configs[self.music]["labels"],
                            self.configs[self.music]["BPM"], self.configs[self.music]["fake_notes"],
                            self.configs[self.music]["slow_notes"], self.configs[self.music]["slow_durations"])
            ]
            self.active_music = self.music_list[self.active_music_idx]
        
        
    def dev_shorts(self, event, notes_to_play, stop_index, round_callback, music_start_pos, change_music):
        
        if event.type == pg.KEYDOWN:
            if event.key == self.developer_keys[0]:
                if not self.active_music.paused:
                    pg.mixer.music.pause()
                    self.active_music.channel.pause()
                    self.active_music.paused = True
                else:
                    pg.mixer.music.unpause()
                    self.active_music.channel.unpause()
                    self.active_music.paused = False
                
            if event.key == self.developer_keys[1]:
                    time_back = float(pg.mixer.music.get_pos()/1000) - 1 + music_start_pos/1000
                    pg.mixer.music.play(start=time_back)
                    if self.active_music.paused: pg.mixer.music.pause()
                    
                    music_start_pos = time_back*1000
                    round_callback(max(0,music_start_pos), True)

                    for i in range(0, stop_index+1):
                        notes_to_play[i].reset()

            if event.key == self.developer_keys[2]:                
                time_forward = float(pg.mixer.music.get_pos()/1000) + 1 + music_start_pos/1000
                pg.mixer.music.play(start=time_forward)
                if self.active_music.paused: pg.mixer.music.pause()
                
                music_start_pos = time_forward*1000   
                round_callback(music_start_pos, False)

            if event.key == self.developer_keys[3]:  
                pg.mixer.music.play(start=0)
                round_callback(0, True)
                

            if event.key == self.developer_keys[4]:  
                self.recording_mode() 
                change_music()

    def read_configs(self):
        with open('./src/config/music_test.json', 'r') as json_file:
            music_data = json.load(json_file)
        return music_data
    
    def write_configs(self, music_data):
        with open('./src/config/music_test.json', 'w') as json_file:
            json.dump(music_data, json_file)
            
    def recording_mode(self):
        self.hidden_music_idx = self.active_music_idx
        self.active_music_idx = (self.hidden_music_idx + 1) % 2
        
        self.configs[self.music]["labels"] = self.music_list[0].labels
        self.configs[self.music]["keyfields"] = self.music_list[0].columns
        
        if len(self.music_list[0].labels) != 0 and self.active_music == self.music_list[0]:             
            self.music_list[1] = PlayerMusic(self.configs[self.music]["music_file"], self.configs[self.music]["speed"],
                        self.configs[self.music]["keyfields"], self.configs[self.music]["labels"],
                        self.configs[self.music]["BPM"], self.configs[self.music]["fake_notes"],
                        self.configs[self.music]["slow_notes"], self.configs[self.music]["slow_durations"])
            self.write_configs(self.configs)
            self.music_list[0] = VoidMusic(self.configs[self.music]["music_file"], self.configs[self.music]["speed"])
            pg.time.wait(500)
        self.active_music = self.music_list[self.active_music_idx]
        return
        
    def draw(self, screen : pg.Surface, music_start_pos, font_size):
        
        a = (60000/(4*self.BPM))
        actual_label = round((pg.mixer.music.get_pos()+music_start_pos)/a)
        font = pg.font.SysFont('Comic Sans MS', font_size*2)
        text =  font.render(str(actual_label), False, (220, 0, 0))
        screen.blit(text, (self.active_music.playgrounds[0].key_fields[0].rect.x - text.get_width()-30, self.active_music.playgrounds[0].key_fields[0].rect.centery))    
        if self.active_music == self.music_list[0]:
            text =  font.render("Recording", False, (220, 0, 0))
            screen.blit(text, (screen.get_width()-text.get_width() - 5, 0))    
       
    
        
    def create_music(self, music_start_pos, column):
        if self.active_music == self.music_list[0]:
            self.music_list[0].columns.append(column) 
            a = (60000/(4*self.BPM))
            label = round((pg.mixer.music.get_pos()+music_start_pos)/a)
            self.music_list[0].labels.append(label)
        
        
