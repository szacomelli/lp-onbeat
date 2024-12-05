import pygame as pg
import notes
import music
import playground
import devmode
import os

class CurrentRound:

    def __init__(self,  music : music.Music, screen_size=[480,640], switch_key=pg.K_SPACE, dev=False):
        # basic atributtes
        """
        Creates a new instance of CurrentRound, which will be responsible for managing one round of the game.

        Parameters:
        music (music.Music): The music to be played in this round.
        screen_size (list): A list containing width and height of the screen.
        switch_key (int): The key that should be used to switch between playgrounds.
        dev (bool): A boolean indicating if the dev mode should be enabled.

        Attributes:
        _screen_size (list): A list containing width and height of the screen.
        active_playground (int): An integer indicating which playground is currently active.
        music_start_pos (int): An integer indicating the current position in the music.
        __dev_active (bool): A boolean indicating if the dev mode should be enabled.
        music (music.Music): The music to be played in this round.
        speed (int): An integer indicating the speed of the notes.
        notes_to_play (list): A list containing all the notes to be played in this round.
        notes_interval (list): A list containing the time intervals between each note.
        start_index (int): An integer indicating which note should be the first one to be played.
        stop_index (int): An integer indicating which note should be the last one to be played.
        max_index (int): An integer indicating the last note to be played.
        font (pg.font.Font): A font object to be used for rendering the text.
        total_points (int): The total points earned in this round.
        combo (int): The current combo.
        _combo_mult_scores (list): A list containing the score multipliers for each combo level.
        _remaining_misses (int): An integer indicating how many misses are left before the game is over.
        game_over (bool): A boolean indicating if the game is over.
        text_x (int): The x position of the text.
        text_y (list): A list containing the y positions of the text.
        text_font (int): An integer indicating the font size of the text.
        combo_txt (pg.Surface): A surface containing the rendered text of the combo.
        score_txt (pg.Surface): A surface containing the rendered text of the score.
        text_ratio (list): A list containing the width and height ratio of the text.
        switch_key (int): The key that should be used to switch between playgrounds.

        """
        if not isinstance(screen_size, list) or len(screen_size) != 2 or not all(isinstance(dim, int) for dim in screen_size):
            raise ValueError("The 'screen_size' parameter must be a list with two integers: [width, height].")
        if not isinstance(switch_key, int):
            raise TypeError("The 'switch_key' parameter must be an integer representing a pygame key.")
        if not isinstance(dev, bool):
            raise TypeError("The 'dev' parameter must be a boolean.")
        

    """
    The custom music created by the player
    
    Attributes
    ----------
    self._screen_size: list[int, int]
    The size of the game screen, represented as (width, height).

    self.active_playground: Playground
        The currently active music playground.

    self.music_start_pos: int
        The millisecond position at which the music starts playing.

    self.__dev_active: bool
        Indicates whether the developer editing mode is active.

    self.music: Music
        The music object containing details about the music to be played.

    self.speed: float
        The speed of the music.

    self.notes_to_play: list
        A list of notes that need to be played during the round.

    self.notes_interval: list[int]
        A list of timestamps (in milliseconds) for when each note should be played.

    self.start_index: int
        The starting position in `notes_to_play` from which the round begins playing.

    self.stop_index: int
        The stopping position in `notes_to_play` at which the round ends playing.

    self.max_index: int
        The maximum index of `notes_to_play`.

    self.total_points: int
        The total score accumulated during the round.

    self.combo: int
        The current combo count for the round.

    self._combo_mult_scores: list[float]
        A list of thresholds for the combo count required to increase the combo multiplier.

    self._remaining_misses: int
        The number of notes that can be missed before the game ends.

    self.game_over: bool
        Indicates whether the current round is over.

    self.text_x: int
        The x-coordinate where all texts related to the `CurrentRound` are drawn.

    self.text_y: list[int]
        A list containing the y-coordinates for the texts related to the `CurrentRound`.

    self.text_font: int
        The font size used for displaying the texts.

    self._combo_txt: str
        A string representing the text for the round's combo.

    self._score_txt: str
        A string representing the text for the round's score.

    self.text_ratio: list[float]
        A list representing the scaling ratio for the displayed texts.

    self.__switch_key: int
        A key used to switch between music playgrounds (if available).
    """
    def __init__(self,  music : music.Music, screen_size=[480,640], switch_key=pg.K_SPACE, dev=False):
        # basic atributtes
>>>>>>> main
        self._screen_size = screen_size
        self.active_playground = 0
        self.music_start_pos = 0
        self.__dev_active = dev
<<<<<<< HEAD

=======
>>>>>>> main
        
        # change the music to dev-selected one. maybe it's better to modularize the dev class to call round, not the other way around
        # also defines some basic attributes for the music and notes
        self.music = music
        self.speed = self.music.speed
        self.notes_to_play = self.music.notes_list
        self.notes_interval = self.music.time_intervals
        self.start_index = 0
        self.stop_index = -1
        self.max_index = len(self.notes_to_play) - 1
<<<<<<< HEAD

        font_path = os.path.join("assets", "8bitoperator.ttf")
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Fonte não encontrada: {font_path}")
        self.font = pg.font.Font(font_path, 20)

=======
        
>>>>>>> main
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
        
<<<<<<< HEAD
        self.msg = ["Miss", "Bad","Great!", "Perfect!",""]
        self.i = 4
        self.messages = [self.font.render(self.msg[0], True, (255, 255, 255)),
                         self.font.render(self.msg[1], True, (255, 255, 255)),
                         self.font.render(self.msg[2], True, (255, 255, 255)),
                         self.font.render(self.msg[3], True, (255, 255, 255)),
                         self.font.render(self.msg[4], True, (255, 255, 255))]
        self.x_pos = 0
        self.y_pos = 0
                      
    # starts the music
    def start_round(self):
        
        """
        Starts the music and prepares the round to be played.

        This method is called when the round should be started. It will call the
        play_music method of the music object, which will start the music and
        prepare it for the round.
        """
        if not hasattr(self.music, 'play_music') or not callable(self.music.play_music):
            raise AttributeError("The 'music' object must have a callable 'play_music' method.")
        self.music.play_music()
        
    # keep track of pressed keys; it's used just for the Stakes level or for dev
    def on_event(self, event):
        """
        Handles events in the round.

        This method is called when an event occurs in the game. It will call the
        dev_shorts method of the dev object if the developer mode is active, and
        will switch the active playground if the switch key is pressed.

        Parameters
        ----------
        event : pygame.event.Event
            The event that occurred.

        Returns
        -------
        None
        """
        if not isinstance(event, pg.event.Event):
            raise TypeError("The 'event' parameter must be an instance of 'pygame.event.Event'.")
        if event.type == pg.KEYDOWN:
            if event.key == self.__switch_key:
                self.active_playground = (self.active_playground + 1) % len(self.music.playgrounds)

    # selects notes that need to be placed in screen                         
=======
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
>>>>>>> main
    def play_notes(self):
        """
        Plays the notes in the notes_to_play list if the current music position is beyond the time interval of the note.

        Returns
        -------
        None
        """
        if not isinstance(self.notes_to_play, list) or not all(isinstance(note, notes.Note) for note in self.notes_to_play):
            raise TypeError("The 'notes_to_play' attribute must be a list of 'notes.Note' instances.")
        if not isinstance(self.notes_interval, list) or not all(isinstance(interval, (int, float)) for interval in self.notes_interval):
            raise TypeError("The 'notes_interval' attribute must be a list of numbers.")
        
        if len(self.notes_to_play) == 0: self.stop_index = self.max_index = -1
        if self.stop_index >= len(self.notes_to_play) - 1: 
            self.stop_index = len(self.notes_to_play) - 2
            self.max_index = self.stop_index
        
        while self.stop_index != self.max_index and pg.mixer.music.get_pos() + self.music_start_pos + (2000/480)*self._screen_size[0] >= self.notes_interval[self.stop_index + 1]:
            self.stop_index += 1
            
            self.notes_to_play[self.stop_index].time_interval = self.notes_interval[self.stop_index]
    
<<<<<<< HEAD
    def draw_objects(self, screen : pg.Surface, keys):        
        """
        Draws all game objects on the screen, including playgrounds, notes, and UI elements.

        Parameters
        ----------
        screen : pg.Surface
            The pygame Surface object where the game objects will be drawn.
        keys : list
            A list of keys that are currently pressed.

        Returns
        -------
        None
        """
=======
    # draw all needed objects
    def draw_objects(self, screen : pg.Surface, keys):
>>>>>>> main
        for playground in self.music.playgrounds:
            playground.draw(screen)
            for key_fields in playground.key_fields:
                key_fields.draw(screen)

        if len(self.notes_to_play) <= self.stop_index: return
        
        for i in range(self.start_index, self.stop_index+1, 1):
            self.notes_to_play[i].draw(screen)
            
<<<<<<< HEAD
        combo_rect = self._combo_txt.get_rect(topleft=(self.text_x, self.text_y[0]))
        score_rect = self._score_txt.get_rect(topleft=(self.text_x, self.text_y[1]))
        unified_rect = combo_rect.union(score_rect).inflate(25, 25)
        pg.draw.rect(screen, (150, 80, 180), unified_rect)
            
        screen.blit(self._combo_txt, (self.text_x, self.text_y[0]))
        screen.blit(self._score_txt, (self.text_x, self.text_y[1]))
        screen.blit(self.messages[self.i], (self.x_pos, self.y_pos))
        
        for playground in self.music.playgrounds:
            playground.make_border(screen)
        

    def on_key_press(self, keys, notes_list, dev = None):        
        """
        Handles key press events for the current round, updating note states and scoring.

        This function checks if any key in the active playground's key fields is pressed and not
        yet marked as pressed. If a key press is detected, it tries to match it with a note 
        in the notes list. If a matching note is found, it updates the note's state, checks for 
        fake or slow notes, and updates the score based on the note's value and current combo 
        multiplier. If no note is matched, it triggers a miss and resets the combo.

        Parameters
        ----------
        keys : list
            A list of boolean values indicating the current state of all keys.
        notes_list : list
            A list of note objects that are being played in the current round.

        Returns
        -------
        None
        """

        if not isinstance(notes_list, list) or not all(isinstance(note, notes.Note) for note in notes_list):
                raise TypeError("The 'notes_list' parameter must be a list of 'notes.Note' instances.")

=======
            self.notes_to_play[i].draw_rect(screen)
        
        screen.blit(self._combo_txt, (self.text_x, self.text_y[0]))
        screen.blit(self._score_txt, (self.text_x, self.text_y[1]))
        

    # keep track of key_fields pressed
    def on_key_press(self, keys, notes_list, dev=None):        
>>>>>>> main
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
<<<<<<< HEAD
                    self.points_message(actual_note, key_field)
                    
                    active_pg = self.music.playgrounds[self.active_playground]
                    pg_rect = active_pg.get_rect()  # Adicione um método `get_rect` em `playground` para obter o rect.
                    self.x_pos = pg_rect.x + (pg_rect.width - self.messages[self.i].get_width()) // 2
                    self.y_pos = pg_rect.y + (pg_rect.height - self.messages[self.i].get_height()) // 2
                    n = actual_note.calculate_points()
                    self.total_points += n*self.calculate_combo_multiplier(self.combo)
=======
                    self.total_points += actual_note.calculate_points()*self.calculate_combo_multiplier(self.combo)
>>>>>>> main
                    self._remaining_misses += 1
                else:
                    if self.__dev_active: 
                        dev.create_music(self.music_start_pos, self.music.playgrounds[self.active_playground].key_fields.index(key_field))
                    key_field.pressed = True
                    self.combo = 0
                    self._remaining_misses -= 1
<<<<<<< HEAD

    def points_message(self, actual_note, key_field):
        """
        Displays a message on the screen based on the points earned by the user for the note
        played. The message is centered on the screen and its position is stored in self.x_pos and
        self.y_pos for later use.

        Parameters
        ----------
        actual_note : note.Note
            The note that was played.
        key_field : keyfields.KeyField
            The key_field that was pressed.

        Returns
        -------
        None
        """
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

        self.x_pos = (self._screen_size[1] - self.messages[self.i].get_width()) // 2
        self.y_pos = (self._screen_size[0] - self.messages[self.i].get_height()) // 2
        
    # just calculates the multiplier the player gets by each hit note
    def calculate_combo_multiplier(self, combo):
        """
        Calculates the combo multiplier of the current combo.

        Parameters
        ----------
        combo : int
            The current combo.

        Returns
        -------
        int
            The combo multiplier, which is 1, 2, 3, or 4, depending on the combo.
        """
        if combo >= self._combo_mult_scores[0] and combo < self._combo_mult_scores[1]: return 1
        elif combo >= self._combo_mult_scores[1] and combo < self._combo_mult_scores[2]: return 2
        elif combo >= self._combo_mult_scores[2] and combo < self._combo_mult_scores[3]: return 3
        elif combo >= self._combo_mult_scores[3]: return 4
    # updates all needed objects
    def update(self, keys, screen, resize, dev = None):
        """
        Updates the state of the current round.

        Parameters
        ----------
        keys : list
            A list of boolean values indicating the current state of all keys.
        screen : pygame.display
            The screen to update.
        resize : boolean
            A boolean indicating whether the screen size has changed.

        Returns
        -------
        boolean
            A boolean indicating whether the round should end.
        """
=======
    
    # just calculates the multiplier the player gets by each hit note
    def calculate_combo_multiplier(self, combo):
        if combo >= self._combo_mult_scores[0] and combo < self._combo_mult_scores[1]: return 1
        elif combo >= self._combo_mult_scores[1] and combo < self._combo_mult_scores[2]: return 2
        elif combo >= self._combo_mult_scores[2] and combo < self._combo_mult_scores[3]: return 3
        elif combo >= self._combo_mult_scores[3]: return 4

    # updates all needed objects
    def update(self, keys, screen, resize, dev=None):
>>>>>>> main
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
<<<<<<< HEAD
                    if not hasSlow: self.start_index += 1      
=======
                    if not hasSlow: self.start_index += 1
                           

        if self.music.has_panning:
            self.music.update()
>>>>>>> main

        if self.total_points < 0: self.total_points = 0
        if self._remaining_misses <= 0: self.game_over = True
        
        self._combo_txt = self.create_text("Combo: ",self.combo)
        self._score_txt = self.create_text("Score: ",self.total_points)
        return False

    # update the ratio (the ratio is between the current and original screen size)
    def update_ratio(self,width_ratio,height_ratio):
        """
        Updates the note ratio and text ratio given the width and height ratios of the screen.
        
        Parameters
        ----------
        width_ratio : float
            The width ratio of the screen.
        height_ratio : float
            The height ratio of the screen.
        
        Returns
        -------
        None
        """
        if not isinstance(width_ratio, (int, float)) or not isinstance(height_ratio, (int, float)):
            raise TypeError("The 'width_ratio' and 'height_ratio' parameters must be numbers.")
        note_ratio = max(width_ratio,height_ratio)
        for note in self.notes_to_play:
            note.ratio = note_ratio
            for interval in note.point_intervals[0]:
                interval = interval * width_ratio
        self.text_ratio = [width_ratio,height_ratio]

    # create a text, used for score and combo
    def create_text(self, text, number):
        """
        Creates a rendered text image given a text string and a number.
        
        Parameters
        ----------
        text : str
            The text string to render.
        number : int
            The number to append to the end of the text string.
        
        Returns
        -------
        pygame.Surface
            The rendered text image.
        """
        if not isinstance(text, str):
            raise TypeError("The 'text' parameter must be a string.")
        if not isinstance(number, (int, float)):
            raise TypeError("The 'number' parameter must be an integer or float.")
        return self.font.render(text + str(number), True, (255, 255, 255))
