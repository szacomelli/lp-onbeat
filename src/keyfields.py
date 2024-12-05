import pygame as pg
from pathlib import Path
import os
import notes
from pathlib import Path
import os


class KeyField:
    def __init__(self, x: int, y: int, unpressed_color, pressed_color, key: int, sprite_path: str, size: int = 30):
        """
        Creates a KeyField object, which is a visual representation of a keyboard key.

        Parameters:
        x (int): The x-coordinate of the top-left corner of the key field.
        y (int): The y-coordinate of the top-left corner of the key field.
        unpressed_color (tuple): A tuple representing the color of the key when it is not pressed.
        pressed_color (tuple): A tuple representing the color of the key when it is pressed.
        key (int): The key that this KeyField object represents.
        sprite_path (str): The path to the sprite that should be used for the key field.
        size (int): The size of the key field. The default is 30.
        """
        interior_size = size-size*(1/6)
        self.bias = -interior_size + size
        self.rect = pg.Rect(x, y, size, size)
        self.unpressed_color = unpressed_color
        self.pressed_color = pressed_color

        self.key = key
        self.pressed = False
        self.sprite_unpressed = MakeSprite(self.rect, sprite_path)
        self.sprite_pressed = MakeSprite(self.rect, f"./assets/notes/keyfield_pressed/pressed_{MakeSprite.identify_sprite(sprite_path)}.png")
        

        screen_height = pg.display.get_surface().get_height()
        self.space_rect = pg.Rect(x, 0, size, screen_height)
        self.sprite_line = MakeSprite(self.space_rect, f"./assets/game_screen/line/center/center_{MakeSprite.identify_sprite(sprite_path)}.png")
        
        
        self.trian_rect = pg.Rect(x, 0, size, size//2)
        self.sprite_trian = MakeSprite(self.trian_rect, f"./assets/game_screen/trian/trian_{MakeSprite.identify_sprite(sprite_path)}.png")
        self.shadow_sup_rect = pg.Rect(0, 0, size, size)
        self.sprite_shadow_sup = MakeSprite(self.shadow_sup_rect, f"./assets/game_screen/shadow/sup/shadow_{MakeSprite.identify_sprite(sprite_path)}.png")
        self.shadow_inf_rect = pg.Rect(x, screen_height, size, screen_height - y)
        self.sprite_shadow_inf = MakeSprite(self.shadow_inf_rect, f"./assets/game_screen/shadow/inf/shadow_inf_{MakeSprite.identify_sprite(sprite_path)}.png")

    def draw(self, display):
        """
        Draws the key field on the given display surface.

        Parameters:
        display (pygame.Surface): The display surface on which to draw the key field.
        """
        self.sprite_line.draw(display)
        self.sprite_shadow_sup.draw(display)
        self.sprite_shadow_inf.draw(display) 
        self.sprite_trian.draw(display)

        if self.pressed:
            self.sprite_pressed.draw(display)
        else:
            self.sprite_unpressed.draw(display)

    def detect_FakeNote(self, note):
        """
        Determines if the given note is a FakeNote.

        Parameters
        ----------
        note : notes.Note
            The note object to be checked.

        Returns
        -------
        bool
            True if the note is an instance of FakeNote, False otherwise.
        """
        if isinstance(note, notes.FakeNote): 
            return True
        else: 
            return False

    def detect_SlowNote(self, note, combo):
        """
        Detects if a SlowNote is being pressed and updates the combo counter accordingly.

        This method checks if the given note is an instance of SlowNote and if it is being pressed.
        It updates the note's state and calculates whether the note holding duration meets the required
        threshold to increase the combo counter. If the threshold is met, the combo is incremented.

        Parameters
        ----------
        note : notes.Note
            The note object to be checked.
        combo : int
            The current combo counter.

        Returns
        -------
        int
            The updated combo counter.
        """
        if isinstance(note, notes.SlowNote):
            if note.pressed == False: note.y_holding_start = note.rect.y
            note.pressed = True
            if note.y_holding_end - note.y_holding_start + 10*note.ratio > note.rect.height : 
                note.updating = False
                return combo + 1
            else: return combo
        else: return combo + 1
        
    def update(self, keys):
        """
        Updates the pressed state of the key field based on the current state of the keys.

        Parameters
        ----------
        keys : list
            A list of boolean values indicating the current state of all keys.

        This method checks the state of the key associated with this KeyField
        object. If the key is not pressed, it sets the `pressed` attribute to False.
        """
        if not keys[self.key]:
            self.pressed = False


class MakeSprite:
    """
    A class used to create and manage sprites in a Pygame application.
    Attributes
    ----------
    rect : pygame.Rect
        Defines the position and size of the sprite on the display surface.
    sprite : pygame.Surface
        The loaded sprite image, initialized from the given file path.

    Methods
    -------
    __init__(rect, sprite_path)
        Initializes the MakeSprite object with a rectangle and a sprite image path.
    load_sprites(filepath: str) -> list
        Class method that loads all sprite file paths from a given directory.
    identify_sprite(sprite_path: str) -> str
        Class method that identifies a sprite based on its file path.
    draw(display)
        Draws the sprite on the given display surface, scaling it to fit the rectangle.
    """
    def __init__(self, rect, sprite_path):
        
        """
        Initializes the MakeSprite object with a rectangle and a sprite image path.

        Parameters
        ----------
        rect : pygame.Rect
            The rectangle defining the position and size of the sprite.
        sprite_path : str
            The file path of the sprite image.

        Raises
        ------
        RuntimeError
            If the Pygame display has not been initialized.
        """
        self.sprite = pg.image.load(sprite_path).convert_alpha()
        self.rect = rect

    @classmethod
    def load_sprites(cls, filepath: str) -> list:
        """
        Class method that retrieves all sprite file paths from a given directory.

        Parameters
        ----------
        filepath : str
            The path of the directory containing the sprite files.

        Returns
        -------
        list
            A sorted list of file paths for the sprite images in the directory.
        """
        sprite_paths = []
        for sprite_file in Path(filepath).iterdir():
            if sprite_file.is_file():
                sprite_paths.append(str(sprite_file))  # Adiciona o caminho do arquivo
        return sorted(sprite_paths)
    @classmethod
    def identify_sprite(cls, sprite_path: str) -> str:
        """
        Class method that extracts an identifier for the sprite from its file name.

        Parameters
        ----------
        sprite_path : str
            The file path of the sprite image.

        Returns
        -------
        str
            The last character of the file name (excluding its extension), 
            which is assumed to be the sprite's identifier.
        """
        nothing_extention = os.path.splitext(sprite_path)[0]
        return nothing_extention[-1]
    
    def draw(self, display):

        """
        Draws the sprite on the display surface.

        Parameters
        ----------
        display : pygame.Surface
            The display surface on which the sprite will be drawn.
        """

        scaled_sprite = pg.transform.scale(self.sprite, self.rect.size)
        display.blit(scaled_sprite, self.rect.topleft)
