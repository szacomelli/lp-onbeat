import pygame as pg
import keyfields
from abc import ABC, abstractmethod
import os

class Note(ABC): 
    def __init__(self, field : keyfields.KeyField, speed=2, intervals=[[0, 10, 20], [5, 3, 1]]):
        """
        Constructor for Note
        
        Parameters
        ----------
        field : keyfields.KeyField
            The key field that this note is associated with
        speed : int
            The speed of the note (default is 2)
        intervals : list
            A 2D list of intervals of each note (default is [[0, 10, 20], [5, 3, 1]])
        """
        
        self.color = field.unpressed_color
        self.speed = speed
        self.destructed = False
        self.field = field
        self.updating = True
        self.point_intervals = intervals
        self.points_args = []
        self.time_interval = 0
        self.ratio = 1

    @abstractmethod
    def draw(self):        
        raise NotImplementedError("You should implement this method")
    
    @abstractmethod
    def update(self):
        raise NotImplementedError("You should implement this method")
    
    @abstractmethod
    def calculate_points(self, speed, starting_pos):
        raise NotImplementedError("You should implement this method")
    
    @abstractmethod
    def note_ended(self):
        raise NotImplementedError("You should implement this method")
    
    def calculate_time_gap(self, starting_pos):
        """
        Calculates the time gap between the current position of the music and the starting position of the note
        
        Parameters
        ----------
        starting_pos : int
            The starting position of the note
            
        Returns
        -------
        int
            The time gap between the current position of the music and the starting position of the note
        """
        return self.time_interval - pg.mixer.music.get_pos() - starting_pos
    
    def reset(self):
        """
        Resets the note to its initial state
        
        Sets self.destructed and self.updating to False and True respectively
        """
        self.destructed = False
        self.updating = True
        
    
class FastNote(Note):
    def __init__(self, field : keyfields.KeyField, id, speed=1, intervals=[[0, 10, 20], [5, 3, 1]]):
        """
        Initializes a FastNote object
        
        Parameters
        ----------
        field : keyfields.KeyField
            The key field on which the note should be drawn
        id : int
            The id of the sprite that should be used for the note
        speed : int, optional
            The speed at which the note should move down the screen by default it is 1
        intervals : list of lists of int, optional
            The intervals at which the note should move down the screen by default it is [[0, 10, 20], [5, 3, 1]]
        
        Attributes
        ----------
        rect : pygame.Rect
            The rectangle of the note
        points_args : list
            A list of arguments that should be used to calculate the points of the note
        sprite : keyfields.MakeSprite
            The sprite of the note
        """
        super().__init__(field, speed, intervals)
        size = self.field.rect.width*(1-1/6)
        self.y_spawn = 0 - size
        self.rect = pg.Rect(field.rect.centerx - size/2, self.y_spawn, size, size)
        self.points_args = [field.rect.y] 

        # sprites
        sprite_path = keyfields.MakeSprite.load_sprites("./assets/notes/fastnotes/")[id]
        self.sprite = keyfields.MakeSprite(self.rect, sprite_path)
        

    def draw(self, display):
        """
        Draws the FastNote on the provided display surface using its sprite.

        Parameters
        ----------
        display : pygame.Surface
            The display surface on which the note should be drawn.

        This method checks if the note is currently active (not destructed) and
        updates its visual representation on the screen using the associated sprite.
        """
        if self.updating == True and self.destructed == False:
            # verify
            # if abs(self.rect.y - self.field.rect.y) <= 10*self.ratio:
            #     pg.draw.rect(display, (255,255,255), self.rect)
            # else:
            #     pg.draw.rect(display, self.color, self.rect)

            # sprites
            self.sprite.draw(display)

    def update(self, speed, starting_pos, label_duration):
        """
        Updates the FastNote's position and checks if it should be destructed.

        Parameters
        ----------
        speed : int
            The speed at which the note should move.
        starting_pos : int
            The starting position of the note.
        label_duration : int
            The duration of the label.

        This method updates the position of the FastNote object by calculating its
        new y-coordinate based on the given speed and the time gap between the
        starting position and the current position of the note. If the note's
        y-coordinate is above the top of the screen (i.e., the note is off the
        screen), the note is marked as destructed (i.e., it should be removed from
        the game).

        This method should be called once per frame to ensure the note's position
        is updated correctly.
        """
        self.rect.centerx = self.field.rect.centerx
        self.rect.width, self.rect.height = self._calculate_size()
        

        self.rect.y = self.field.rect.y - (self.calculate_time_gap(starting_pos))/speed#+= self.speed
        if self.field.rect.bottom + 10 < self.rect.top:
            self.destructed = True
                
    def calculate_points(self):
        """
        Calculates the points for the note based on its vertical bias from the target field.

        The function determines the bias between the y-coordinate of the note's rectangle
        and the y-coordinate of the field's rectangle. It then compares this bias against
        predefined intervals to decide the points the note should receive. The closer the
        bias is to zero, the higher the points awarded.

        Returns
        -------
        int
            The points awarded for the note based on its vertical position. Possible values
            are from the second list in `self.point_intervals` or 1 if the bias falls outside
            all specified intervals.
        """
        bias = self.field.rect.y - self.rect.y
        if bias <= self.point_intervals[0][0] and bias >= -self.point_intervals[0][0]: return self.point_intervals[1][0]
        elif bias <= self.point_intervals[0][1] and bias >= -self.point_intervals[0][1]: return self.point_intervals[1][1]
        elif bias <= self.point_intervals[0][2] and bias >= -self.point_intervals[0][2]: return self.point_intervals[1][2]
        else: return 1

    def _calculate_size(self):
        """
        Calculates the size of the note based on the size of its associated key field.
        
        Returns
        -------
        tuple
            A tuple containing the width and height of the note. The width is the same as the width of the key field and the height is the same as the height of the key field.
        """
        return (self.field.rect.width,self.field.rect.height)

    def note_ended(self):
        """
        Determines if the note has reached the end of its lifecycle.

        This method checks whether the note has completed its intended
        duration or position within the field. It returns a boolean
        indicating if the note should be considered ended.

        Returns
        -------
        bool
            True if the note has ended, False otherwise.
        """
        return True

class SlowNote(Note):
    def __init__(self, field : keyfields.KeyField, id, speed=1,intervals=[[0, 10, 20], [5, 3, 1]], height=150):
        """
        Initializes a SlowNote object.

        Parameters
        ----------
        field : keyfields.KeyField
            The key field associated with the note.
        id : int
            The identifier for selecting the appropriate sprite folder.
        speed : int, optional
            The speed at which the note should move, default is 1.
        intervals : list of lists of int, optional
            The intervals at which the note should move, default is [[0, 10, 20], [5, 3, 1]].
        height : int, optional
            The height of the note, default is 150.

        Attributes
        ----------
        height : int
            The height of the note.
        height_ratio : float
            The ratio of the note's height to its width.
        rect : pygame.Rect
            The rectangle defining the note's boundaries.
        pressed : bool
            Whether the note is pressed.
        y_holding_start : int
            The starting y-coordinate for holding the note.
        y_holding_end : int
            The ending y-coordinate for holding the note.
        top_selected : bool
            Whether the top of the note is selected.
        first_update : bool
            Whether this is the first update of the note.
        sprite_sections : list
            The list of sprite sections for the note's visual representation.
        """
        super().__init__(field, speed, intervals)
        self.height = height
        width = self.field.rect.width*(1-1/6)
        self.height_ratio = height/width
        
        self.y_spawn = 0 - height
        self.rect = pg.Rect(field.rect.centerx - width/2, self.y_spawn, width, height)

        self.pressed = False
        self.y_holding_start = 0
        self.y_holding_end = 0
        
        self.top_selected = False
        self.first_update = True

        # sprites
        self.sprite_sections = []
        num_sprites = int(self.height_ratio)
        self.sprite_heigth = self.height / num_sprites
        filepath = "./assets/notes/slownotes/"

        folders = sorted([folder for folder in os.listdir(filepath) if os.path.isdir(os.path.join(filepath, folder))])
        if not (0 <= id < len(folders)):
            raise ValueError(f"The 'id={id}' index is out of the valid range (0 to {len(folders) - 1}).")
        sprite_folder = os.path.join(filepath, folders[id])
        sprite_files = sorted([file for file in os.listdir(sprite_folder) if os.path.isfile(os.path.join(sprite_folder, file))])
        sprite_dict = {0: 3, num_sprites - 1: 0, num_sprites // 2: 2}

        for i in range(num_sprites):
            sprite_rect = pg.Rect(self.rect.x, self.rect.y + i * self.sprite_heigth, width, self.sprite_heigth)
            sprite_path = os.path.join(sprite_folder, sprite_files[sprite_dict.get(i, 1)])
            self.sprite_sections.append(keyfields.MakeSprite(sprite_rect, sprite_path))

    def draw(self, display):
        """
        Draws the SlowNote object on the given display surface.

        Parameters
        ----------
        display : pygame.display
            The display surface to draw the note on.

        Notes
        -----
        This method draws each sprite in the sprite_sections list on the display surface.
        """
        if self.updating == True:# and self.destructed == False:
            # pg.draw.rect(display, self.color, self.rect)
            for sprite in self.sprite_sections:
                sprite.draw(display)

    def update(self, speed, starting_pos, label_duration):
        """
        Updates the SlowNote object according to the given speed, starting position, and label duration.
        
        Parameters
        ----------
        speed : int
            The speed at which the note should move down the screen
        starting_pos : int
            The position on the y-axis where the note should start moving down the screen
        label_duration : int
            The duration of the note in terms of frames
        
        Notes
        -----
        This method updates the visual representation of the note and checks if it should be destructed.
        """

        self.rect.height = (int((self.rect.height*self.speed)/label_duration))*label_duration/self.speed + self.rect.width
        self.height_ratio = self.rect.height/self.rect.width
        self.speed = speed
        self.rect.centerx = self.field.rect.centerx
        self.rect.width, self.rect.height = self._calculate_size()
        self.rect.bottom = self.field.rect.bottom- (self.calculate_time_gap(starting_pos))/speed 

        # sprites
        sprite_height = self.rect.height / len(self.sprite_sections)
        for i, sprite in enumerate(self.sprite_sections):
            sprite.rect.x = self.rect.x
            sprite.rect.y = self.rect.y + i * sprite_height
            sprite.rect.width = self.rect.width
            sprite.rect.height = sprite_height


        # verify
        if self.field.rect.bottom + 50*self.ratio < self.rect.top:# and not self.pressed:
            self.pressed = False
            self.destructed = True
                
    def calculate_points(self):
        """
        Calculates the points of the SlowNote object based on the time it was held.

        Returns
        -------
        int
            The points of the SlowNote object.
        """
        
        if self.y_holding_end - self.y_holding_start + 10*self.ratio > self.rect.height : 
            return 5
        else: return 0

    def reset(self):
        """
        Resets the SlowNote object back to its initial state. This is called when
        the note is either pressed and held, or when the note is not pressed at all.
        """
        
        self.destructed = False
        self.updating = True
        self.pressed = False
        self.y_holding_start = 0
        self.y_holding_end = 0

    def _calculate_size(self):
        """
        Calculates the size of the SlowNote object based on the field's width and the height ratio.

        Returns
        -------
        tuple
            A tuple containing the width and height of the SlowNote object.
        """
        return (self.field.rect.width,self.field.rect.width*self.height_ratio)
    
    def note_ended(self):
        """
        Checks if the note has ended based on its position and the field's bottom edge.

        Returns
        -------
        bool
            True if the note has ended, False otherwise.
        """
        if self.rect.top + self.ratio*10 >= self.field.rect.bottom:
            self.y_holding_end = self.rect.y
            return True
        else:
            return False

class FakeNote(Note):
    def __init__(self, field : keyfields.KeyField, id, speed=2, intervals=[[0, 10, 20], [5, 3, 1]]):
        """
        Initializes a FakeNote object.

        Parameters
        ----------
        field : keyfields.KeyField
            The key field associated with the note.
        id : int
            The identifier for selecting the appropriate sprite.
        speed : int, optional
            The speed at which the note should move, default is 2.
        intervals : list of lists of int, optional
            The intervals at which the note should move, default is [[0, 10, 20], [5, 3, 1]].

        Attributes
        ----------
        rect : pygame.Rect
            The rectangle defining the note's boundaries.
        color : tuple
            The color of the note, derived from the field's unpressed color.
        sprite : keyfields.MakeSprite
            The sprite representing the note's visual appearance.
        """
        super().__init__(field, speed, intervals)
        height = self.field.rect.width - self.field.bias
        self.y_spawn = 0 - height
        self.rect = pg.Rect(field.rect.x + 5, self.y_spawn, 20, height)
        self.color = tuple(element/2 for element in self.field.unpressed_color)

        sprite_path = keyfields.MakeSprite.load_sprites("./assets/notes/fakenotes/")[id]
        self.sprite = keyfields.MakeSprite(self.rect, sprite_path)
        

    def draw(self, display):
        """
        Draws the FakeNote object on the given display surface.

        Parameters
        ----------
        display : pygame.Surface
            The display surface on which to draw the FakeNote object.

        Notes
        -----
        This method checks if the note has been destructed and if not draws the sprite on the display surface.
        """
        if self.updating:
            # pg.draw.rect(display, self.color, self.rect)
            # Adding sprite drawing
            self.sprite.draw(display)

    def update(self,speed, starting_pos, label_duration):
        """
        Updates the FakeNote's position and marks it for destruction if necessary.

        Parameters
        ----------
        speed : int
            The speed at which the note should move.
        starting_pos : int
            The starting position of the note on the y-axis.
        label_duration : int
            The duration of the label in terms of frames.

        Notes
        -----
        This method updates the note's position on the screen based on the given
        speed and starting position. It also checks if the note has moved off the
        screen and marks it as destructed if so. This method should be called once
        per frame while the note is being updated.
        """


    def update(self,speed, starting_pos, label_duration):
            self.rect.centerx = self.field.rect.centerx
            self.rect.width, self.rect.height = self._calculate_size()
            

            self.rect.y = self.field.rect.y - (self.calculate_time_gap(starting_pos))/speed#+= self.speed
            if self.field.rect.bottom + 10 < self.rect.top:
                self.destructed = True
                self.updating = False                
                

    def calculate_points(self):
        """
        Calculates the points earned by the user for this note.

        Returns
        -------
        int
            The points earned by the user for this note.
        """
        
        return -1
    
    def _calculate_size(self):
        """
        Calculates the size of the FakeNote based on the dimensions of the associated key field.

        Returns
        -------
        tuple
            A tuple containing the width and height of the FakeNote, determined by the
            width and height of the key field's rectangle.
        """
        return (self.field.rect.width,self.field.rect.height)
    
    def note_ended(self):
        """
        Checks if the note has ended.

        Returns
        -------
        bool
            True if the note has ended, False otherwise.
        """
        return True
