import pygame as pg
import music
import json
import playground as pgr
import notes as nt
import currentround as cr

pg_numbers = [1,1]

playgrounds = [pgr.Playground(50,640,480,keys=[pg.K_d,pg.K_f,pg.K_j,pg.K_k], blank_space_percentage=0.1,pg_numbers=pg_numbers)]


class VoidMusic(music.Music):
    def __init__(self, file, speed, bpm):
        self.paused = False
        self.label_duration = 60000/(4*bpm)
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
    def __init__(self, file, speed, int_columns, labels, bpm, fake_notes, slow_notes, slow_heights, file_delay):
        self.paused = False
        
        self.file_delay = file_delay
        self.bpm = bpm
        self.label_duration = (60000/(4*self.bpm))
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
            intervals.append(i*label_length + self.file_delay) 
        return intervals
    
    def create_notes(self, playgrounds : list[pgr.Playground]):
        note_list = self.int_to_notes(playgrounds[0].key_fields,self.columns,self.slow_notes,self.fake_notes,self.slow_heights)
        return note_list


class DevMode:
    
    def __init__(self, music_name, keys=[[pg.K_d,pg.K_f,pg.K_j,pg.K_k]],dkeys=[pg.K_LSHIFT, pg.K_q, pg.K_e, pg.K_r, pg.K_m, pg.K_LEFT, pg.K_RIGHT,
                                                                               pg.K_UP, pg.K_DOWN, pg.K_RETURN, pg.K_DELETE, pg.K_INSERT, pg.K_p], active=False, editing_music=False):
        self.configs = self.read_configs()
        self.music_info = self.configs[music_name]
        
        if editing_music: self.edit_music(music_name)
        if self.configs.keys().isdisjoint([music_name]): self.new_music(music_name)
        
        self.music = music_name
        self.active = active
        self.developer_keys = dkeys
        self.active_music_idx = 1
        self.hidden_music_idx = 0
        self.BPM = self.music_info["BPM"]
        

        if self.active:
            self.music_list = [
                VoidMusic(self.music_info["music_file"], self.music_info["speed"], self.BPM),
                PlayerMusic(self.music_info["music_file"], self.music_info["speed"],
                            self.music_info["keyfields"], self.music_info["labels"],
                            self.music_info["BPM"], self.music_info["fake_notes"],
                            self.music_info["slow_notes"], self.music_info["slow_durations"], 
                            self.music_info["file_delay"])
            ]
            self.active_music = self.music_list[self.active_music_idx]
        self.index_selected = 0
        self.editing_note = False
        self.max_visible_index = 0
        self.min_visible_index = 0
        
        self.round = cr.CurrentRound(self.active_music, dev=True)
    
    def edit_music(self, name):
        self.configs[name]["music_file"] = input("new music file path: ")
        self.configs[name]["speed"] = 10/int(input("new speed: "))
        self.configs[name]["BPM"] = int(input("new bpm: "))
        self.configs[name]["file_delay"] = int(input("new music delay: "))
        self.write_configs(self.configs)
    
    def new_music(self, name):
            bpm = input("music bpm: ")
            speed = input("music speed: ")
            path = input("path (relative to the game folder lp-onbeat): ")
            delay = input("(moment where the music actually starts, in millisenconds): ")
            self.configs[name] = {
            "music_file": "./",
            "file_delay" : 0,
            "BPM": 0,
            "labels": [],
            "notes": [],
            "keyfields": [],
            "slow_notes": [],
            "slow_durations": [],
            "fake_notes": [],
            "speed": 1
        }
            self.configs[name]["music_file"] = path
            self.configs[name]["speed"] = 10/int(speed)
            self.configs[name]["keyfields"] = []
            self.configs[name]["labels"] = []
            self.configs[name]["file_delay"] = int(delay)
            self.configs[name]["BPM"] = int(bpm)
            self.configs[name]["fake_notes"] = []
            self.configs[name]["slow_notes"] = []
            self.configs[name]["slow_durations"] = []
            self.write_configs(self.configs)
    
        
    def dev_shorts(self, event, notes_to_play, max_index, stop_index, round_callback, music_start_pos):
        
        if event.type == pg.KEYDOWN:
            if event.key == self.developer_keys[0]:
                if not self.active_music.paused:
                    pg.mixer.music.pause()
                    self.active_music.channel.pause()
                    self.active_music.paused = True
                    self.index_selected = self.max_visible_index
                else:
                    pg.mixer.music.unpause()
                    self.active_music.channel.unpause()
                    self.active_music.paused = False
                    self.editing_note = False
                    self.max_visible_index = 0
                
            if event.key == self.developer_keys[1]:
                if not self.active_music.paused:
                    time_back = float(pg.mixer.music.get_pos()/1000) - 1 + music_start_pos/1000
                    pg.mixer.music.play(start=time_back)
                    if self.active_music.paused: pg.mixer.music.pause()
                    
                    music_start_pos = time_back*1000
                    round_callback(max(0,music_start_pos), True, False)

                    for i in range(0, stop_index+1):
                        notes_to_play[i].reset()

            if event.key == self.developer_keys[2]:        
                if not self.active_music.paused:   
                    time_forward = float(pg.mixer.music.get_pos()/1000) + 1 + music_start_pos/1000
                    pg.mixer.music.play(start=time_forward)
                    if self.active_music.paused: pg.mixer.music.pause()
                    
                    music_start_pos = time_forward*1000   
                    round_callback(music_start_pos, False, False)

            if event.key == self.developer_keys[3]:
                if not self.active_music.paused:
                    self.max_visible_index = 0
                    pg.mixer.music.play(start=0)
                    round_callback(0, True, False)
                    
            if event.key == pg.K_0:
                pg.mixer.quit()
                pg.mixer.init(44100, size=-2)
                self.active_music.play_music()
            
            if event.key == pg.K_9:
                pg.mixer.quit()
                pg.mixer.init(44100)
                self.active_music.play_music()
            
            if event.key == self.developer_keys[4]:  
                self.recording_mode() 
                #change_music()
                
            if event.key == self.developer_keys[5]:  
                if self.editing_note:
                    self.change_note_position(-1, notes_to_play, max_index, music_start_pos)
                    
            if event.key == self.developer_keys[6]:  
                if self.editing_note:
                    self.change_note_position(1, notes_to_play, max_index, music_start_pos)
                
            if event.key == self.developer_keys[7]:  
                if self.editing_note:
                    self.change_note_position(2, notes_to_play, max_index, music_start_pos)
                else:
                    self.change_selection(max_index, False, notes_to_play)
                
            if event.key == self.developer_keys[8]:  
                if self.editing_note:
                    self.change_note_position(-2, notes_to_play, max_index, music_start_pos)
                else:
                    self.change_selection(max_index, True, notes_to_play)

            if event.key == self.developer_keys[9]:
                if self.editing_note:
                    self.editing_note = False
                else:
                    self.editing_note = True
            
            if event.key == self.developer_keys[10]:
                self.destruct_note(notes_to_play)
                round_callback(music_start_pos, False, True)
            
            if event.key == self.developer_keys[11]:
                self.add_note(notes_to_play)
            
            if event.key == self.developer_keys[12]:
                if self.editing_note: self.change_note_type(notes_to_play)
    
    def change_note_type(self, notes):
        idx = self.index_selected
        current_note = notes[idx]
        speed = current_note.speed
        note_interval = current_note.time_interval
        
        if isinstance(current_note, nt.FastNote): 
            notes[self.index_selected] = nt.SlowNote(current_note.field)
            self.music_info["slow_notes"].append(self.index_selected)
            notes[self.index_selected].height_ratio = 1
            self.music_info["slow_durations"].append(notes[self.index_selected].height_ratio)
        elif isinstance(current_note, nt.SlowNote): 
            notes[self.index_selected] = nt.FakeNote(current_note.field)
            self.music_info["slow_durations"].pop(self.music_info["slow_notes"].index(self.index_selected))
            self.music_info["slow_notes"].remove(self.index_selected)
            self.music_info["fake_notes"].append(self.index_selected)
        elif isinstance(current_note, nt.FakeNote): 
            notes[self.index_selected] = nt.FastNote(current_note.field)
            self.music_info["fake_notes"].remove(self.index_selected)

        notes[idx].speed = speed
        notes[idx].time_interval = note_interval
        notes[idx].rect.y = current_note.rect.y
        notes[idx].rect.width = current_note.rect.width
        notes[idx].ratio = current_note.ratio
            
    def change_note_position(self, direction, notes, max_index, music_starting_pos):
        labels = self.music_info["labels"]
        columns = self.music_info["keyfields"]
        if len(notes) == 0: 
            return
        # up and down
        if direction == 2:
            note = notes[self.index_selected]
            if isinstance(notes[self.index_selected], nt.SlowNote):
                if note.top_selected:
                    note.rect.height += self.music_list[1].label_duration/note.speed
                    note.height_ratio = note.rect.height/note.rect.width
                    idx = self.music_info["slow_notes"].index(self.index_selected)
                    self.music_info["slow_durations"][idx] = note.height_ratio
                else:
                    if note.rect.height != note.rect.width:
                        notes[self.index_selected].time_interval += self.music_list[1].label_duration
                        labels[self.index_selected] += 1
                        note.rect.height -= self.music_list[1].label_duration/(note.speed)
                        note.height_ratio = note.rect.height/note.rect.width
                        while labels[self.index_selected] > labels[self.index_selected + 1]:
                            self.update_configs(notes, self.index_selected, 1, True)
                            self.index_selected += 1
            else:
                notes[self.index_selected].time_interval += self.music_list[1].label_duration
                labels[self.index_selected] += 1
                while self.index_selected != max_index and labels[self.index_selected] > labels[self.index_selected + 1]:
                    self.update_configs(notes, self.index_selected, 1, False)
                    self.index_selected += 1 
        elif direction == -2:
            note = notes[self.index_selected]
            if isinstance(notes[self.index_selected], nt.SlowNote):
                if not note.top_selected:
                    note.rect.height += self.music_list[1].label_duration/(note.speed)
                    notes[self.index_selected].time_interval -= self.music_list[1].label_duration
                    labels[self.index_selected] -= 1
                    note.height_ratio = note.rect.height/note.rect.width
                    while self.index_selected != 0 and labels[self.index_selected] < labels[self.index_selected - 1]:
                        self.update_configs(notes, self.index_selected, -1, True)
                        self.index_selected -= 1                        
                else:
                    if note.rect.height != note.rect.width:
                        note.rect.height -= self.music_list[1].label_duration/note.speed
                        note.height_ratio = note.rect.height/note.rect.width
                        idx = self.music_info["slow_notes"].index(self.index_selected)
                        self.music_info["slow_durations"][idx] = note.height_ratio
            else:
                notes[self.index_selected].time_interval -= self.music_list[1].label_duration
                self.music_info["labels"][self.index_selected] -= 1
                #while the label of selected is less than the previous
                while self.index_selected != 0 and labels[self.index_selected] < labels[self.index_selected - 1]:
                    self.update_configs(notes, self.index_selected, -1, False)
                    self.index_selected -= 1
            
        #left and right
        elif direction == 1:
            idx = (playgrounds[0].key_fields.index(notes[self.index_selected].field) + 1 )% 4
            notes[self.index_selected].field = playgrounds[0].key_fields[idx]
            notes[self.index_selected].color = notes[self.index_selected].field.unpressed_color
            columns[self.index_selected] = (columns[self.index_selected] + 1) % 4    
        elif direction == -1:
            idx = (playgrounds[0].key_fields.index(notes[self.index_selected].field) - 1 )% 4
            notes[self.index_selected].field = playgrounds[0].key_fields[idx]
            notes[self.index_selected].color = notes[self.index_selected].field.unpressed_color
            columns[self.index_selected] = (columns[self.index_selected] - 1) % 4
        
    def update_configs(self, notes, idx, value, isSlow):
        swap_idx = idx + value
        if isSlow:
            slow_idx = self.music_info["slow_notes"].index(idx)
            self.music_info["slow_notes"][slow_idx] += value
            self.music_info["slow_durations"][slow_idx] = notes[self.index_selected].height_ratio
        self.music_info["labels"][idx], self.music_info["labels"][swap_idx] =\
            self.music_info["labels"][swap_idx], self.music_info["labels"][idx]
        self.music_info["keyfields"][idx], self.music_info["keyfields"][swap_idx] =\
            self.music_info["keyfields"][swap_idx], self.music_info["keyfields"][idx]
        notes[idx], notes[swap_idx] = notes[swap_idx], notes[idx]

    def destruct_note(self, notes : list[int]):
        if len(notes) != 0 and len(notes) > self.index_selected:
            self.music_info["labels"].pop(self.index_selected)
            self.music_info["keyfields"].pop(self.index_selected)
            if isinstance(notes[self.index_selected], nt.SlowNote):
                idx = self.music_info["slow_notes"].index(self.index_selected)
                self.music_info["slow_notes"].pop(idx)
                self.music_info["slow_durations"].pop(idx)
            if isinstance(notes[self.index_selected], nt.FakeNote):
                idx = self.music_info["fake_notes"].index(self.index_selected)
                self.music_info["fake_notes"].pop(idx)
            notes.pop(self.index_selected)

    def add_note(self, notes : list):
        idx = self.index_selected
        if len(notes) == 0:
            new_note = nt.FastNote(self.active_music.playgrounds[0].key_fields[0])
            label = round(pg.mixer.music.get_pos()/self.active_music.label_duration)
            new_note.time_interval = label*self.active_music.label_duration
            notes.insert(0, new_note)
            self.music_info["labels"].insert(0, label)
            self.music_info["keyfields"].insert(0, 0)
        else:
            new_note = nt.FastNote(notes[self.index_selected].field)
            new_note.time_interval = notes[self.index_selected].time_interval + self.music_list[1].label_duration
            notes.insert(self.index_selected + 1, new_note)
            label = new_note.time_interval/self.music_list[1].label_duration
            self.music_info["labels"].insert(self.index_selected+1, label)
            column = self.music_info["keyfields"][idx]
            self.music_info["keyfields"].insert(self.index_selected+1, column)
    
    def change_selection(self, max_index, down, notes):
        if len(notes) == 0: 
            return
        if down: 
            if isinstance(notes[self.index_selected], nt.SlowNote):
                if notes[self.index_selected].top_selected:
                    notes[self.index_selected].top_selected = False
                    return
             
            self.index_selected = max(0,self.index_selected - 1)
            if isinstance(notes[self.index_selected], nt.SlowNote): 
                notes[self.index_selected].top_selected = True
                
        else: 
            if isinstance(notes[self.index_selected], nt.SlowNote):
                if not notes[self.index_selected].top_selected:
                    notes[self.index_selected].top_selected = True
                    return
                else: 
                    notes[self.index_selected].top_selected = False
            
            self.index_selected = min((self.index_selected + 1), max_index)
            if isinstance(notes[self.index_selected], nt.SlowNote): notes[self.index_selected].top_selected = False
             
    def draw_selection(self, screen, notes : list[nt.Note], music_start_pos, stop_index, round_callback):
        if self.active_music.paused and len(notes) > self.index_selected:
            note = notes[self.index_selected]
            rect_bottom = note.rect.bottom
            rect_y = note.rect.y
            if isinstance(note, nt.SlowNote):
                if note.top_selected: 
                    rect_bottom = note.rect.y - note.rect.width
                else:
                    rect_y = rect_bottom - note.rect.width
            
            # shifts the screen up/down in case the note has gone too high or low
            if rect_bottom >  note.field.rect.bottom:
                time_back = float(pg.mixer.music.get_pos()/1000) - 0.25 + music_start_pos/1000
                pg.mixer.music.play(start=time_back)
                if self.active_music.paused: 
                    pg.mixer.music.pause()
                    
                music_start_pos = time_back*1000
                round_callback(max(0,music_start_pos), True, False)
                for i in range(0, stop_index+1):
                    notes[i].reset()
            elif rect_y <= 0:
                time_forward = float(pg.mixer.music.get_pos()/1000) + 1 + music_start_pos/1000
                pg.mixer.music.play(start=time_forward)
                if self.active_music.paused: 
                    pg.mixer.music.pause()
                    
                music_start_pos = time_forward*1000   
                round_callback(music_start_pos, False, False)
                
            # draw the selection
            left = note.rect.x - 5*note.ratio
            size = note.rect.width+10*note.ratio
            if isinstance(note, nt.SlowNote):
                if note.top_selected:
                    precise_rect = pg.rect.Rect(left, note.rect.top - 5*note.ratio, size, size)
                    pg.draw.rect(screen, (255,255,255), precise_rect, width=round(note.ratio))
                else:
                    precise_rect = pg.rect.Rect(left, note.rect.bottom - note.rect.width - 5*note.ratio, size, size)
                    pg.draw.rect(screen, (255,255,255), precise_rect, width=round(note.ratio))
            else:
                rect = pg.rect.Rect(left, note.rect.y- 5*note.ratio, size, note.rect.height+10*note.ratio)
                pg.draw.rect(screen, (255,255,255), rect, width=round(note.ratio))
    
    def read_configs(self):
        with open('./src/config/music_test.json', 'r') as json_file:
            music_data = json.load(json_file)
        return music_data
    
    def write_configs(self, music_data):
        with open('./src/config/music_test.json', 'w') as json_file:
            json.dump(music_data, json_file)
            
    def recording_mode(self):
        self.write_configs(self.configs)
        self.hidden_music_idx = self.active_music_idx
        self.active_music_idx = (self.hidden_music_idx + 1) % 2
        if len(self.music_list[0].labels) != 0:    
            self.music_info["labels"] = self.music_list[0].labels
            self.music_info["keyfields"] = self.music_list[0].columns
            self.music_info["slow_notes"] = []
            self.music_info["slow_durations"] = []
            self.music_info["fake_notes"] = []
            self.write_configs(self.configs)
        
        if self.active_music == self.music_list[0]:             
            self.music_list[1] = PlayerMusic(self.music_info["music_file"], self.music_info["speed"],
                        self.music_info["keyfields"], self.music_info["labels"],
                        self.music_info["BPM"], self.music_info["fake_notes"],
                        self.music_info["slow_notes"], self.music_info["slow_durations"],
                        self.music_info["file_delay"])
            self.music_list[0] = VoidMusic(self.music_info["music_file"], self.music_info["speed"], self.BPM)
                        
        self.active_music = self.music_list[self.active_music_idx]
        speed, txt_x, txt_y, font, txt_ratio = self.round.speed, self.round.text_x, self.round.text_y, self.round.text_font, self.round.text_ratio
        self.round = cr.CurrentRound(self.active_music, dev=True)
        self.round.speed, self.round.text_x, self.round.text_y, self.round.text_font, self.round.text_ratio = speed, txt_x, txt_y, font, txt_ratio
        self.round.start_round()
        return
        
    def on_event(self, event):
        self.dev_shorts(event, self.round.notes_to_play, self.round.max_index, self.round.stop_index, self.round.round_callback, self.round.music_start_pos)        
        self.round.on_event(event)
        
    def draw(self, screen : pg.Surface, music_start_pos, font_size):
        krect = self.active_music.playgrounds[0].key_fields[0].rect
        a = (60000/(4*self.BPM))
        actual_label = round((pg.mixer.music.get_pos()+music_start_pos - self.music_list[1].file_delay)/a)
        font = pg.font.SysFont('Comic Sans MS', font_size*2)
        text =  font.render(str(max(0,actual_label)), False, (220, 0, 0))
        screen.blit(text, (krect.x - text.get_width()-30, krect.centery))    
        if self.active_music == self.music_list[0]:
            text =  font.render("Recording", False, (220, 0, 0))
            screen.blit(text, (screen.get_width()-text.get_width() - 5, 0))    
       
    
        
    def create_music(self, music_start_pos, column):
        if self.active_music == self.music_list[0] and pg.mixer.music.get_busy():
            self.music_list[0].columns.append(column) 
            a = (60000/(4*self.BPM))
            label = round((pg.mixer.music.get_pos()+music_start_pos-self.music_list[1].file_delay)/a)
            self.music_list[0].labels.append(label)
        
        
