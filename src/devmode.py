import pygame as pg
import music
import json
import playground as pgr
import notes as nt
import currentround as cr


pg_numbers = [1,1]
pg.init()
screen = pg.display.set_mode((800, 600))

playgrounds = [pgr.Playground(50,640,480,keys=[pg.K_d,pg.K_f,pg.K_j,pg.K_k], blank_space_percentage=0.1,pg_numbers=pg_numbers)]


class VoidMusic(music.Music):
    """
    A music that doesn't have notes. It's used to record new notes to the music.
    
    Attributes
    ----------
    self.paused : bool
        If the music is paused
    self.label_duration : int
        How many milisecons a note lasts
    self._file_path : str
        Path to the music file
    self.notes_list : list
        List of music notes
    self.labels : list
        The labels of each note
    self._columns : list
        The key field column where each note plays
    self.time_intervals : list
        List of intervals of each note
    self.multiplayer_info : list
        A list containing the multiplayer information 
    self.total_notes : int
        Number of total notes of the music
    self.speed : int
        The speed of the music
    self.playgrounds : list
        A list containing all the playgrounds the music utilizes
    self._song : pygame.mixer.Sound
        The music initialized as a Sound
    self._channel pg.mixer.Channel
        A pygame channel for the sound version of the song
    self.has_panning : bool
        A boolean representing if the song has panning
    self.length : int
        Length of the music in miliseconds
    """
    def __init__(self, file, speed, bpm):
        """
        Constructor for VoidMusic
        
        Parameters
        ----------
        file : str
            Path to the music file
        speed : int
            Speed of the music
        bpm : int
            BPM of the music
        """
        
        self.paused = False
        self.label_duration = 60000/(4*bpm)
        self._file_path = file
        self.notes_list = []
        self.labels = []
        self._columns = []
        self.time_intervals = []
        self.multiplayer_info = [False, 1]
        self.total_notes = 0
        self.speed = speed
        self.playgrounds = playgrounds
        self._song = pg.mixer.Sound(file)
        self._channel = pg.mixer.Channel(1)
        self.has_panning = False
        a = pg.mixer.Sound(self._file_path)
        self.length = a.get_length()
        
    def _create_intervals(self):
        """
        Returns a list of intervals (in miliseconds) that represent the duration of
        each note in the music. The intervals are calculated based on the BPM of
        the music and the duration of each label (in miliseconds)
        """
        return []
    
    def _create_notes(self, playgrounds):
        """
        Generates a list of notes for the music based on the provided playgrounds.

        Parameters
        ----------
        playgrounds : list
            A list containing playground objects, each representing a musical environment 
            where notes can be placed.

        Returns
        -------
        list
            A list of note objects created for the music.
        """
        return []

class PlayerMusic(music.Music):
    """
    The custom music created by the player
    
    Attributes
    ----------
    self.bpm : int
        BPM of the music
    self._fake_notes : list
        List representing what notes are Fake Notes
    self._slow_notes : list
        List representing what notes are Slow Notes
    self._slow_heights : list
        List with the heights of the notes
    self.paused : bool
        If the music is paused
    self.label_duration : int
        How many milisecons a note lasts
    self._file_path : str
        Path to the music file
    self.notes_list : list
        List of music notes
    self._labels : list
        The labels of each note
    self._columns : list
        The key field column where each note plays
    self.time_intervals : list
        List of intervals of each note
    self.multiplayer_info : list
        A list containing the multiplayer information 
    self.total_notes : int
        Number of total notes of the music
    self.speed : int
        The speed of the music
    self.playgrounds : list
        A list containing all the playgrounds the music utilizes
    self._song : pygame.mixer.Sound
        The music initialized as a Sound
    self._channel pg.mixer.Channel
        A pygame channel for the sound version of the song
    self.has_panning : bool
        A boolean representing if the song has panning
    self.length : int
        Length of the music in miliseconds
    """
    def __init__(self, file, speed, int_columns, labels, bpm, fake_notes, slow_notes, slow_heights, file_delay):
        
        self.paused = False
        self.file_delay = file_delay
        self.bpm = bpm
        self.label_duration = (60000/(4*self.bpm))
        self._columns = int_columns
        self._fake_notes = fake_notes
        self._slow_notes = slow_notes
        self._slow_heights = slow_heights    
        self.playgrounds = playgrounds
        self.multiplayer_info = [False, 1]
        self._file_path = file
        
        self.notes_list = self._create_notes(self.playgrounds)
        self._labels = labels
        self.time_intervals = self._create_intervals()
        
        self.total_notes = len(self.notes_list)
        self.speed = speed
        
        
        self._song = pg.mixer.Sound(file)
        self.channel = pg.mixer.Channel(1)
        self.has_panning = False
        a = pg.mixer.Sound(self._file_path)
        self.length = a.get_length()
        
        
    def _create_intervals(self):
        """
        Creates a list of intervals in miliseconds, that represent the duration of
        each note in the music. The intervals are calculated based on the BPM of
        the music and the duration of each label (in miliseconds)
        """
        
        intervals = []
        
        for i in self._labels:
            intervals.append(i*self.label_duration + self.file_delay) 
        return intervals
    
    def _create_notes(self, playgrounds : list[pgr.Playground]):
        """
        Generates a list of notes for the music based on the provided playgrounds.

        Parameters
        ----------
        playgrounds : list[pgr.Playground]
            A list containing playground objects, each representing a musical environment 
            where notes can be placed.

        Returns
        -------
        list
            A list of note objects created for the music.
        """
        note_list = self._int_to_notes(playgrounds[0].key_fields,self._columns,self._slow_notes,self._fake_notes,self._slow_heights)
        return note_list


class DevMode:
    def __init__(self, music_name, keys=[[pg.K_d,pg.K_f,pg.K_j,pg.K_k]],dkeys=[pg.K_LSHIFT, pg.K_q, pg.K_e, pg.K_r, pg.K_m, pg.K_LEFT, pg.K_RIGHT,
                                                                               pg.K_UP, pg.K_DOWN, pg.K_RETURN, pg.K_DELETE, pg.K_INSERT, pg.K_p], active=False, editing_music=False):
        """
        Constructor for DevMode
        
        Parameters
        ----------
        music_name : str
            Name of the music to be edited/created
        keys : list
            List of lists of keys to be used by the music
        dkeys : list
            List of keys to be used by the developer
        active : bool
            A boolean indicating whether the music is already active
        editing_music : bool
            A boolean indicating whether the music is being edited
            
        Attributes
        ----------
        self.configs : dict
            All the player musics information
        self.music_info : dict
            Information of current music
        self.music_list : list
            List containing Player and Void music
        self.music : str
            Music name
        self.developer_keys : list
            List with the keyboard keys used by edit mode
        self.active_music_idx : int
            Index of the active music in music list
        self.hidden_music_idx : int
            Index of the non-active music in music list
        self.BPM : int
            Music BPM
        self.max_visible_index : int
            Index of the last note in screen
        self.min_visible_index : int
            Index of first visible note in screen
        self.round : cr.CurrentRound
            The round the DevMode class manages
        """
        
        self.configs = self.__read_configs()
        self.music_info = self.configs[music_name]
        
        
        self.music = music_name
        self.developer_keys = dkeys
        self.active_music_idx = 1
        self.hidden_music_idx = 0
        self.BPM = self.music_info["BPM"]
        

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
    
    def _edit_music(self, name):
        """
        Allows the user to edit an existing music, changing its file path, speed, BPM and file delay.
        
        Parameters
        ----------
        name : str
            Name of the music to be edited
        """
        
        self.configs[name]["music_file"] = input("new music file path: ")
        self.configs[name]["speed"] = 10/int(input("new speed: "))
        self.configs[name]["BPM"] = int(input("new bpm: "))
        self.configs[name]["file_delay"] = int(input("new music delay: "))
        self.__write_configs(self.configs)
    
    def _new_music(self, name):
        """
        Creates a new music and adds it to the music config file.
        
        Parameters
        ----------
        name : str
            Name of the music to be created
        """
        
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
        self.__write_configs(self.configs)
    
    def dev_shorts(self, event, notes_to_play, max_index, stop_index, music_start_pos):
        
        """
        Handles developer shortcut keys for controlling music playback and editing notes.
        
        Parameters
        ----------
        event : pygame.event.Event
            The event object containing information about keyboard input.
        notes_to_play : list
            A list of note objects currently being played.
        max_index : int
            The maximum index for the notes to play.
        stop_index : int
            The index at which note playback should stop.
        music_start_pos : float
            The starting position of the music in milliseconds.
        
        This method allows developers to control music playback (pause, play, rewind, fast-forward)
        and edit notes using specific keys defined in `developer_keys`. It also includes functionalities
        for quitting and reinitializing the music mixer and handling recording mode.
        """
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
                    self.__round_att_update(max(0,music_start_pos), True, False)

                    for i in range(0, stop_index+1):
                        notes_to_play[i].reset()

            if event.key == self.developer_keys[2]:        
                if not self.active_music.paused:   
                    time_forward = float(pg.mixer.music.get_pos()/1000) + 1 + music_start_pos/1000
                    pg.mixer.music.play(start=time_forward)
                    if self.active_music.paused: pg.mixer.music.pause()
                    
                    music_start_pos = time_forward*1000   
                    self.__round_att_update(music_start_pos, False, False)

            if event.key == self.developer_keys[3]:
                if not self.active_music.paused:
                    self.max_visible_index = 0
                    pg.mixer.music.play(start=0)
                    self.__round_att_update(0, True, False)
                    
            if event.key == pg.K_0:
                pg.mixer.quit()
                pg.mixer.init(44100, size=-2)
                self.active_music.play_music()
            
            if event.key == pg.K_9:
                pg.mixer.quit()
                pg.mixer.init(44100)
                self.active_music.play_music()
            
            if event.key == self.developer_keys[4]:  
                self.__recording_mode() 
                #change_music()
                
            if event.key == self.developer_keys[5]:  
                if self.editing_note:
                    self.__change_note_position(-1, notes_to_play, max_index)
                    
            if event.key == self.developer_keys[6]:  
                if self.editing_note:
                    self.__change_note_position(1, notes_to_play, max_index)
                
            if event.key == self.developer_keys[7]:  
                if self.editing_note:
                    self.__change_note_position(2, notes_to_play, max_index)
                else:
                    self.__change_selection(max_index, False, notes_to_play)
                
            if event.key == self.developer_keys[8]:  
                if self.editing_note:
                    self.__change_note_position(-2, notes_to_play, max_index)
                else:
                    self.__change_selection(max_index, True, notes_to_play)

            if event.key == self.developer_keys[9]:
                if self.editing_note:
                    self.editing_note = False
                else:
                    self.editing_note = True
            
            if event.key == self.developer_keys[10]:
                self.__destruct_note(notes_to_play)
                self.__round_att_update(music_start_pos, False, True)
            
            if event.key == self.developer_keys[11]:
                self.__add_note(notes_to_play)
            
            if event.key == self.developer_keys[12]:
                if self.editing_note: self.__change_note_type(notes_to_play)
                
    def __round_att_update(self, music_start_pos, restart_index, decrease_stop_index):
        """
        Updates round attributes based on music position and index flags.

        Parameters
        ----------
        music_start_pos : int
            The starting position of the music in milliseconds.
        restart_index : bool
            Flag indicating whether to reset the start index of the round.
        decrease_stop_index : bool
            Flag indicating whether to decrease the stop index of the round.

        This method resets all notes to their initial state, updates the music
        start position, and adjusts indices based on the provided flags.
        """
        if restart_index: self.round.start_index = 0
        for note in self.round.notes_to_play:
            note.reset()
        self.round.music_start_pos = music_start_pos
        if decrease_stop_index: self.round.stop_index -= 1
    
    def __change_note_type(self, notes):
        """
        Changes the type of a note in the music editor.

        Parameters
        ----------
        notes : list
            The list of notes to be edited.

        This method changes the type of the selected note in the music editor. If the note is a fast note, it changes
        the note to a slow note. If the note is a slow note, it changes the note to a fake note. If the note is a fake note, it
        changes the note to a fast note.
        """
        
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
            
    def __change_note_position(self, direction, notes, max_index):
        """
        Changes the position of a note in the music editor.

        Parameters
        ----------
        direction : int
            The direction of the change. 1 means right, -1 means left, 2 means up, and -2 means down.
        notes : list
            The list of notes to be edited.
        max_index : int
            The maximum index of the notes list, used to determine whether the selected note is at the end of the list.

        This method changes the position of the selected note in the music editor. If the note is a slow note, it
        also changes the height of the note. If the note is a fast note, it only changes the time interval of the note.
        If the note is a fake note, it does not change the position of the note.
        """
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
                            self.__update_configs(notes, self.index_selected, 1, True)
                            self.index_selected += 1
            else:
                notes[self.index_selected].time_interval += self.music_list[1].label_duration
                labels[self.index_selected] += 1
                while self.index_selected != max_index and labels[self.index_selected] > labels[self.index_selected + 1]:
                    self.__update_configs(notes, self.index_selected, 1, False)
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
                        self.__update_configs(notes, self.index_selected, -1, True)
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
                    self.__update_configs(notes, self.index_selected, -1, False)
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
        
    def __update_configs(self, notes, idx, value, isSlow):
        """
        Updates the configuration of the music editor when a note is swapped.

        Parameters
        ----------
        notes : list
            The list of notes to be swapped
        idx : int
            Index of the note to be swapped
        value : int
            The amount to swap the note
        isSlow : bool
            Whether the note is slow or not

        Notes
        -----
        This method updates the configuration of the music editor when a note is swapped.
        It swaps the note at index idx with the note at index idx + value.
        If the note is slow, it also swaps the duration of the slow note.
        """
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

    def __destruct_note(self, notes : list[int]):
        """
        Removes a note from the specified list and updates the music_info accordingly.

        Parameters
        ----------
        notes : list[int]
            The list of notes from which a note will be removed. The note at the 
            current index_selected will be removed.

        Notes
        -----
        - If the selected note is a SlowNote, it also removes the note from the 
        slow_notes and slow_durations lists in the music_info.
        - If the selected note is a FakeNote, it also removes the note from the 
        fake_notes list in the music_info.
        - The method assumes that index_selected is a valid index for the notes list.
        """
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

    def __add_note(self, notes : list):
        """
        Adds a new note to the specified list and updates the music_info accordingly.
        
        Parameters
        ----------
        notes : list
            The list of notes to which a new note will be added. The new note will be
            added to the index selected by index_selected.
        
        Notes
        -----
        - If the notes list is empty, a new note will be added at the beginning of the list.
        - If the selected note is a SlowNote, the new note will be added after it.
        - The method assumes that index_selected is a valid index for the notes list.
        """
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
    
    def __change_selection(self, max_index, down, notes):
        """
        Changes the selection of a note in the music editor.

        Parameters
        ----------
        max_index : int
            The maximum index of the notes list, used to determine whether the selected note is at the end of the list.
        down : bool
            Whether the selection should move down or up.
        notes : list
            The list of notes to be edited.

        If the selected note is a SlowNote, this method changes the top_selected attribute of the selected note and the
        note above/below it. If the selected note is not a SlowNote, this method only changes the index_selected attribute
        of the DevMode object.
        """
        
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
             
    def draw_selection(self, screen, notes : list[nt.Note], music_start_pos, stop_index):
        """
        Draws and manages the selection rectangle for a note in the music editor.

        Parameters
        ----------
        screen : pygame.Surface
            The screen surface on which the selection rectangle should be drawn.
        notes : list[nt.Note]
            The list of notes currently being edited.
        music_start_pos : float
            The starting position of the music in milliseconds.
        stop_index : int
            The index at which note processing should stop.

        This method handles the drawing of a selection rectangle around the currently selected
        note, ensuring it remains visible on the screen. It shifts the screen's view up or down 
        when the selected note goes beyond the visible boundaries. Additionally, it modifies the 
        selection rectangle's shape based on the note type and selection state.
        """
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
                self.__round_att_update(max(0,music_start_pos), True, False)
                for i in range(0, stop_index+1):
                    notes[i].reset()
            elif rect_y <= 0:
                time_forward = float(pg.mixer.music.get_pos()/1000) + 1 + music_start_pos/1000
                pg.mixer.music.play(start=time_forward)
                if self.active_music.paused: 
                    pg.mixer.music.pause()
                    
                music_start_pos = time_forward*1000   
                self.__round_att_update(music_start_pos, False, False)
                
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
    
    def __read_configs(self):
        """
        Reads the music configuration data from a JSON file.

        This method reads the 'music_test.json' file in the 'src/config' directory and returns
        the contents as a dictionary.

        Returns
        -------
        dict
            The music configuration data read from the JSON file.
        """
        with open('./src/config/music_test.json', 'r') as json_file:
            music_data = json.load(json_file)
        return music_data
    
    def __write_configs(self, music_data):
        """
        Writes the provided music data to a JSON configuration file.

        Parameters
        ----------
        music_data : dict
            A dictionary containing the music configuration data to be written to the JSON file.

        This method opens the 'music_test.json' file in write mode and writes the contents
        of `music_data` to it as a JSON object, overwriting any existing content.
        """
        with open('./src/config/music_test.json', 'w') as json_file:
            json.dump(music_data, json_file)
            
    def __recording_mode(self):
        """
        Toggles the recording mode of the music editor.

        This method is used to switch between the two music tracks in the music editor, and to
        save the edited music data to the configuration file. If the user is currently editing
        the void music track, this method will overwrite the player music track with the edited
        data. If the user is currently editing the player music track, this method will overwrite
        the void music track with the edited data.

        This method is called when the user presses the 'Tab' key while in the music editor. It
        is also called when the user closes the music editor window.

        Parameters
        ----------
        self : DevMode
            The DevMode object that this method is a part of.

        Returns
        -------
        None
        """
        self.__write_configs(self.configs)
        self.hidden_music_idx = self.active_music_idx
        self.active_music_idx = (self.hidden_music_idx + 1) % 2
        if len(self.music_list[0].labels) != 0:    
            self.music_info["labels"] = self.music_list[0].labels
            self.music_info["keyfields"] = self.music_list[0].columns
            self.music_info["slow_notes"] = []
            self.music_info["slow_durations"] = []
            self.music_info["fake_notes"] = []
            self.__write_configs(self.configs)
        
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
        """
        Handles an event by invoking developer shortcuts and updating the round state.

        This method processes an incoming event by calling the `dev_shorts` method, which handles 
        developer-specific keyboard shortcuts, and then delegates further event handling to the 
        `on_event` method of the `round` object.

        Parameters
        ----------
        event : pygame.event.Event
            The event that occurred, typically a keyboard or mouse event.

        Returns
        -------
        None
        """
        self.dev_shorts(event, self.round.notes_to_play, self.round.max_index, self.round.stop_index, self.round.music_start_pos)        
        self.round.on_event(event)   
    def draw(self, screen : pg.Surface, music_start_pos, font_size):
        """
        Draws the current label and "Recording" status on the screen.

        This method renders the current label of the music and the "Recording" status
        (if the active music is VoidMusic) on the screen. The label is drawn on top of
        the first key field of the first playground of the active music, and the "Recording"
        status is drawn at the top-right corner of the screen.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw on.
        music_start_pos : int
            The start position of the music in milliseconds.
        font_size : int
            The size of the font to use for rendering the text.

        Returns
        -------
        None
        """
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
        """
        Records a music column and label based on the current playback position.

        This method appends the specified column to the active music's column list and calculates the 
        corresponding label based on the current position of the music playback. The label is then 
        appended to the active music's label list.

        Parameters
        ----------
        music_start_pos : int
            The start position of the music in milliseconds.
        column : Any
            The column to be recorded in the music's column list.

        Returns
        -------
        None
        """
        if self.active_music == self.music_list[0] and pg.mixer.music.get_busy():
            self.music_list[0].columns.append(column) 
            a = (60000/(4*self.BPM))
            label = round((pg.mixer.music.get_pos()+music_start_pos-self.music_list[1].file_delay)/a)
            self.music_list[0].labels.append(label)
        
        
