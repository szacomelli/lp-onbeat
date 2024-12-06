import pygame as pg
import currentround as ar, music as ms, keyfields as kf
from abc import ABC, abstractmethod
import json

with open("src/languages.json", "r", encoding="utf-8") as file:
    LANGUAGES = json.load(file)
    
with open('./src/config/music_test.json', 'r') as json_file:
    music_data = json.load(json_file)
    
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
class Button:
    def __init__(self, x: float, y: float, width:float, height: float, text:str, font:str, color_hover = (255,25,25), text_color = (255,255,255), texture_path: str=None):
        """
        Initializes a Button object (a representation of a button in a Pygame).

        Parameters
        ----------
        x : float
            The x-coordinate of the top-left corner of the button.
        y : float
            The y-coordinate of the top-left corner of the button.
        width : float
            The width of the button.
        height : float
            The height of the button.
        text : str
            The text that should appear on the button.
        font : str
            The path to the font file that should be used for rendering the button text.
        color_hover : tuple, optional
            A tuple representing the color of the button when the mouse is hovering over it. Defaults to (255,25,25).
        text_color : tuple, optional
            A tuple representing the color of the button text. Defaults to (255,255,255).
        texture_path : str, optional
            The path to the button texture image. If omitted, the button will be rendered as a solid color.

        Notes
        -----
        The button will be rendered as a solid color if no texture_path is provided.
        """
        self.rect = pg.Rect(x, y, width, height)
        self.color_normal = (150, 80, 180)
        self.color_hover = color_hover
        self.text = text
        self.font = font
        self.text_color = text_color
        self.hovered = False

        if texture_path:
            self.texture = pg.image.load(texture_path).convert_alpha()
            self.texture = pg.transform.scale(self.texture, (width, height))
        else:
            self.texture = None

    def draw(self, screen):
        """
        Draws the button on the screen.

        Parameters
        ----------
        screen : pygame.Surface
            The surface on which the button should be drawn.

        Notes
        -----
        If the button has a texture, it will be drawn at its position on the screen.
        Otherwise, the button will be drawn as a solid color.
        """

        if self.texture:
            screen.blit(self.texture, self.rect.topleft)
        else:
            color = self.color_hover if self.hovered else self.color_normal
            pg.draw.rect(screen, color, self.rect)

        if self.hovered and self.texture:
            hover_surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
            hover_surface.fill(self.color_hover)
            screen.blit(hover_surface, self.rect.topleft)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def __check_hover(self, mouse_pos):
        """
        Checks if the mouse is hovering over the button.

        Parameters
        ----------
        mouse_pos : tuple
            The current position of the mouse.

        Notes
        -----
        This method updates the `hovered` attribute of the button.
        """
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        """
        Checks if the button was clicked.

        Parameters
        ----------
        event : pygame.event.Event
            The event that was triggered.

        Returns
        -------
        bool
            True if the button was clicked, False otherwise.

        Notes
        -----
        This method first checks if the mouse is hovering over the button.
        If the event is a mouse button down event, and the mouse is hovering
        over the button, it returns True. Otherwise, it returns False.
        """
        if event.type == pg.MOUSEMOTION:
            self.__check_hover(event.pos)
            return False
        elif event.type == pg.MOUSEBUTTONDOWN and self.hovered and event.button == 1:
            return True
        return False
    
class Screen(ABC):
    def __init__(self, manager):
        """
        Initializes the Screen object.

        Parameters
        ----------
        manager : GameManager
            The GameManager object that is in charge of switching between screens.

        Notes
        -----
        This method sets the fonts and loads the background image for the screen.
        The image is then scaled to fit the screen size.
        """
        self.manager = manager
        self.fonte_title_game = pg.font.Font("./assets/8bitoperator.ttf", 45)       
        self.fonte_title = pg.font.Font("./assets/8bitoperator.ttf", 35)
        self.fonte_subtitle = pg.font.Font("./assets/8bitoperator.ttf", 20)
        self.fonte_subsubtitle = pg.font.Font("./assets/8bitoperator.ttf", 17)
        self.imagem_original = pg.image.load("./assets/game_screen/fundo.png")
        self.imagem = pg.transform.scale(self.imagem_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def translate(self, key_path, language):
        """
        Translates a key path into a string based on the language.

        Parameters
        ----------
        key_path : str
            A string representing a path to a key in the LANGUAGES dictionary.
        language : str
            The language to translate the text into.

        Returns
        -------
        str
            The translated string. If no translation is found, the key_path is returned unchanged.

        Notes
        -----
        The key_path is split into a list of strings using the "." as a separator.
        The function then searches the LANGUAGES dictionary for the corresponding value.
        If no translation is found, the key_path is returned unchanged.
        """

        keys = key_path.split(".")
        text = LANGUAGES[language]
        for key in keys:
            text = text.get(key, None)
            if text is None:
                return key_path
        return text

    @abstractmethod
    def resize(self, screen):
        """
        Resizes the background image to fit the screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the background image for.

        Notes
        -----
        The width and height of the screen are used to resize the background image.
        The resized image is then stored in the `imagem` attribute.
        """
        self.width, self.height = screen.get_size()
        self.imagem = pg.transform.scale(self.imagem_original, (self.width, self.height))

    @abstractmethod
    def draw(self, screen):
        """
        Draws the Screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the background image for.
        """
        pass

    @abstractmethod
    def update(self, screen):
        """
        Updates the Screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the background image for.
        """
        pass

    @abstractmethod
    def on_event(self, screen):
        """
        Handle events in the Screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the background image for.
        """
        pass
    
class MainMenu(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
        """
        Initializes the main menu screen.

        Parameters
        ----------
        button_width : int
            The width of the buttons.
        button_height : int
            The height of the buttons.
        manager : Manager
            The manager of the game.

        Notes
        -----
        The buttons are created and stored in the `dict_buttons` attribute.
        The `name_buttons` attribute is used to translate the button names into the selected language.
        The `loading_message` attribute is used to display the game title during the loading screen.
        """
        super().__init__(manager)
        self.button_width = button_width
        self.button_height = button_height
        self.dict_buttons = {}
        self.name_buttons = self.translate("main_menu.buttons", self.manager.language)
        self.dict_buttons["start"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[0], self.fonte_title)
        self.dict_buttons["settings"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + (self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[1], self.fonte_title)
        self.dict_buttons["ModDev"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + 2*(self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[2], self.fonte_title)
        self.dict_buttons["Help"] = Button(SCREEN_WIDTH - 60, SCREEN_HEIGHT - 60,\
                                             50,50, self.name_buttons[3], self.fonte_title)
        self.dict_buttons["Exit"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + 3*(self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[4], self.fonte_title)
        self.loading_message = self.fonte_title_game.render("OnBeat!!", True, (255, 255, 255))

    def resize(self, screen):
        """
        Resizes the buttons to fit the new screen size.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the buttons for.

        Notes
        -----
        The buttons are resized and repositioned to fit the new screen size.
        The `width` and `height` attributes are used to determine the position of the buttons.
        The `button_width` and `button_height` attributes are used to determine the size of the buttons.
        """
        super().resize(screen)
        self.dict_buttons["start"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["start"].rect.y = (self.height//9) + 120
        self.dict_buttons["settings"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["settings"].rect.y = (self.height//9) + (self.button_height + 10) + 120
        self.dict_buttons["ModDev"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["ModDev"].rect.y = (self.height//9) + 2*(self.button_height + 10) + 120
        self.dict_buttons["Help"].rect.x = self.width - 60
        self.dict_buttons["Help"].rect.y = self.height - 60
        self.dict_buttons["Exit"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["Exit"].rect.y = (self.height//9) + 3*(self.button_height + 10) + 120
    
    def draw(self, screen):
        """
        Draws the main menu screen on the given screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to draw the main menu on.

        Notes
        -----
        The screen is first resized to fit the new screen size, if necessary.
        The background image is then drawn on the screen.
        The main menu buttons are then drawn on the screen.
        Finally, the display is updated to make the changes visible.
        """
        self.resize(screen)
        screen.blit(self.imagem, (0, 0))
        screen.blit(self.loading_message, (self.width//2 - self.loading_message.get_width()//2, self.height//9 + 10))
        self.dict_buttons["start"].draw(screen)
        self.dict_buttons["settings"].draw(screen)
        self.dict_buttons["ModDev"].draw(screen)
        self.dict_buttons["Help"].draw(screen)
        self.dict_buttons["Exit"].draw(screen)
        pg.display.flip()

    def start_game(self, option):
        """
        Changes the game state based on the selected option.

        Parameters
        ----------
        option : int
            The selected option that determines the next game state.

        Notes
        -----
        - Option 1 transitions to the music catalog screen.
        - Option 2 transitions to the settings screen.
        - Option 3 transitions to the development screen.
        - Option 4 transitions to the help screen.
        - Option 5 stops the game by setting the running flag to False.
        """
        if option == 1:
            self.manager.change_state("music_catalog")
        elif option == 2:
            self.manager.change_state("settings")
        elif option == 3:
            self.manager.change_state("dev")
        elif option == 4:
            self.manager.change_state("help")
        elif option == 5:
            self.manager.is_running = False

    def update(self, screen):
        """
        Updates the main menu screen with the current language.

        Parameters
        ----------
        screen : pygame.display
            The screen to update the main menu on.

        Notes
        -----
        The button names are translated into the selected language.
        The `name_buttons` attribute is used to store the translated button names.
        The `dict_buttons` attribute is updated with the translated button names.
        """
        self.name_buttons = self.translate("main_menu.buttons", self.manager.language)
        self.dict_buttons["start"].text = self.name_buttons[0]
        self.dict_buttons["settings"].text = self.name_buttons[1]
        self.dict_buttons["ModDev"].text = self.name_buttons[2]
        self.dict_buttons["Help"].text = self.name_buttons[3]
        self.dict_buttons["Exit"].text = self.name_buttons[4]

    def on_event(self, event, screen):
        """
        Handles events in the main menu screen.

        Parameters
        ----------
        event : pygame.event.Event
            The event that occurred.
        screen : pygame.display
            The screen to update the main menu on.

        Notes
        -----
        If the event is a mouse click, the method checks if the click was on one of the buttons.
        If the click was on a button, the method calls the start_game method with the corresponding option.
        """
        if self.dict_buttons["start"].is_clicked(event):
            self.start_game(1)
        if self.dict_buttons["settings"].is_clicked(event):
            self.start_game(2)
        if self.dict_buttons["ModDev"].is_clicked(event):
            self.start_game(3)
        if self.dict_buttons["Help"].is_clicked(event):
            self.start_game(4)
        if self.dict_buttons["Exit"].is_clicked(event):
            self.start_game(5)
            
class Help(Screen):
    
    def __init__(self, button_width:int, button_height:int, manager):
        """
        Initializes the help screen.

        Parameters
        ----------
        button_width : int
            The width of the buttons.
        button_height : int
            The height of the buttons.
        manager : Manager
            The manager of the game.

        Notes
        -----
        The buttons are created and stored in the `dict_buttons` attribute.
        The `name_button` attribute is used to translate the button name into the selected language.
        The `loading_message` attribute is used to display the game title during the loading screen.
        """
        super().__init__(manager)
        self.button_width = button_width
        self.button_height = button_height
        self.dict_buttons = {}
        self.name_button = self.translate("help.button", self.manager.language)
        self.dict_buttons["back"]= Button(SCREEN_WIDTH//2 - self.button_width//2, SCREEN_HEIGHT - self.button_height//3,\
                                           self.button_width, self.button_height, self.name_button[0], self.fonte_title)
        self.loading_message = self.fonte_title_game.render("OnBeat!!", True, (255, 255, 255))

    def resize(self, screen):
        """
        Resizes the buttons to fit the new screen size.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the buttons for.

        Notes
        -----
        The buttons are resized and repositioned to fit the new screen size.
        The `width` and `height` attributes are used to determine the position of the buttons.
        The `button_width` and `button_height` attributes are used to determine the size of the buttons.
        """
        super().resize(screen)
        self.dict_buttons["back"].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons["back"].rect.y = self.height - (5*self.button_height)//3

    def draw(self, screen):
        """
        Draws the help screen on the given screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to draw the help screen on.

        Notes
        -----
        The screen is cleared and the background image is drawn.
        The loading message is drawn at the top of the screen.
        The button is drawn at the bottom of the screen.
        The display is updated to show the drawn screen.
        """
        self.resize(screen)
        screen.blit(self.imagem, (0, 0))
        screen.blit(self.loading_message, (self.width//2 - self.loading_message.get_width()//2, self.height//9 + 10))
        self.dict_buttons["back"].draw(screen)
        pg.display.flip()

    def start_game(self, option):
        """
        Starts a new game based on the given option.

        Parameters
        ----------
        option : int
            The option to start the game with. 1 for the main menu.

        Notes
        -----
        The game state is changed to the option given.
        """
        if option == 1:
            self.manager.change_state("main_menu")

    def update(self, screen):
        """
        Updates the help screen based on the given screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to update the help screen on.

        Notes
        -----
        The name of the button is updated based on the current language.
        """
        self.name_buttons = self.translate("help.button", self.manager.language)
        self.dict_buttons["back"].text = self.name_buttons[0]

    def on_event(self, event:pg.event.Event,screen):
        """
        Handles events in the help screen.

        Parameters
        ----------
        event : pygame.event.Event
            The event that occurred.
        screen : pygame.display
            The screen to update the help screen on.

        Notes
        -----
        If the event is a mouse click, the method checks if the click was on the back button.
        If the click was on the button, the method starts the game with the main menu option.
        """
        if self.dict_buttons["back"].is_clicked(event):
            self.start_game(1)
            
class Settings(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
        """
        Initializes the settings screen.

        Parameters
        ----------
        button_width : int
            The width of the buttons.
        button_height : int
            The height of the buttons.
        manager : Manager
            The manager of the game.

        Notes
        -----
        The buttons are created and stored in the `dict_buttons` attribute.
        The `name_buttons` attribute is used to translate the button names into the selected language.
        The `loading_message` attribute is used to display the game title during the loading screen.
        """
        super().__init__(manager)
        self.button_width = button_width
        self.button_height = button_height
        self.name_buttons = self.translate("settings.buttons", self.manager.language)
        self.dict_buttons = {}
        self.dict_buttons["language"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[0], self.fonte_title)
        self.dict_buttons["keys"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + (self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[1], self.fonte_title)
        self.dict_buttons["back"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + 2*(self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[2], self.fonte_title)
        self.loading_message = self.fonte_title_game.render("OnBeat!!", True, (255, 255, 255))

    def resize(self, screen):
        """
        Resizes the buttons to fit the new screen size.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the buttons for.

        Notes
        -----
        The buttons are resized and repositioned to fit the new screen size.
        The `width` and `height` attributes are used to determine the position of the buttons.
        The `button_width` and `button_height` attributes are used to determine the size of the buttons.
        """
        super().resize(screen)
        self.dict_buttons["language"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["language"].rect.y = (self.height//9) + 120
        self.dict_buttons["keys"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["keys"].rect.y = (self.height//9) + (self.button_height + 10) + 120
        self.dict_buttons["back"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["back"].rect.y = (self.height//9) + 2*(self.button_height + 10) + 120

    def draw(self, screen):
        """
        Draws the settings screen on the given screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to draw the settings screen on.

        Notes
        -----
        The method first resizes the buttons to fit the new screen size.
        Then, it draws the background image and the buttons on the screen.
        Finally, it updates the display to show the drawn screen.
        """
        self.resize(screen)
        screen.blit(self.imagem, (0, 0))
        screen.blit(self.loading_message, (self.width//2 - self.loading_message.get_width()//2, self.height//9 + 10))
        self.dict_buttons["language"].draw(screen)
        self.dict_buttons["keys"].draw(screen)
        self.dict_buttons["back"].draw(screen)
        pg.display.flip()

    def start_game(self, option):
        """
        Starts a new game based on the given option.

        Parameters
        ----------
        option : int
            The option to start the game with. The options are:
                1. Switch language.
                2. Change keys.
                3. Go back to the main menu.

        Notes
        -----
        The method changes the language of the game if the option is 1.
        The method changes the state of the game to "key" if the option is 2.
        The method changes the state of the game to "main_menu" if the option is 3.
        """
        if option == 1:
            self.manager.language = "English" if self.manager.language == "pt/br" else "pt/br"
        if option == 2:
            self.manager.change_state("key")
        if option == 3:
            self.manager.change_state("main_menu")

    def update(self, screen):
        """
        Updates the settings screen to reflect the current language.

        Parameters
        ----------
        screen : pygame.display
            The screen to update the settings screen on.

        Notes
        -----
        The method translates the button names into the selected language.
        The method sets the text of the buttons to the translated names.
        """
        self.name_buttons = self.translate("settings.buttons", self.manager.language)
        self.dict_buttons["language"].text = self.name_buttons[0]
        self.dict_buttons["keys"].text = self.name_buttons[1]
        self.dict_buttons["back"].text = self.name_buttons[2]

    def on_event(self, event, screen):
        """
        Handles events in the settings screen.

        Parameters
        ----------
        event : pygame.event.Event
            The event that occurred.
        screen : pygame.display
            The screen to update the settings menu on.

        Notes
        -----
        If a button is clicked, the method calls the start_game method with the corresponding option.
        Option 1 switches the language, option 2 changes keys, and option 3 goes back to the main menu.
        """
        if self.dict_buttons["language"].is_clicked(event):
            self.start_game(1)
        if self.dict_buttons["keys"].is_clicked(event):
            self.start_game(2)
        if self.dict_buttons["back"].is_clicked(event):
            self.start_game(3)
            
class MusicCatalog(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
        """
        Initializes the music catalog screen.

        Parameters
        ----------
        button_width : int
            The width of the buttons.
        button_height : int
            The height of the buttons.
        manager : Manager
            The manager of the game.

        Notes
        -----
        The buttons are created and stored in the `dict_buttons` attribute.
        The `name_buttons` attribute is used to translate the button names into the selected language.
        The `name_buttons_player` attribute is used to translate the player button names into the selected language.
        The `dict_buttons_music` attribute is used to translate the music names into the selected language.
        The `index` attribute is used to keep track of the selected music index.
        The `index_player` attribute is used to keep track of the selected player index.
        """
        super().__init__(manager)
        self.button_width = button_width
        self.button_height = button_height
        self.name_buttons = self.translate("music_catalog.buttons", self.manager.language)
        self.name_buttons_player = self.translate("music_catalog.player", self.manager.language)
        self.name_player = ["1player", "2player"]
        self.dict_buttons_music= {}
        self.dict_buttons= {}
        for music in self.manager.music_names:
            music_name = music
            self.dict_buttons_music[music] = Button(SCREEN_WIDTH//2 - self.button_width//2, (SCREEN_HEIGHT//9) + 120,\
                                                     self.button_width, self.button_height, music_name, self.fonte_subtitle)
        self.dict_buttons[self.name_player[0]] = Button(SCREEN_WIDTH//2 - self.button_width//2, (SCREEN_HEIGHT//9) + (self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons_player, self.fonte_subtitle)
        self.dict_buttons[self.name_player[1]] = Button(SCREEN_WIDTH//2 - self.button_width//2, (SCREEN_HEIGHT//9) + (self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons_player[0], self.fonte_subtitle)
        self.dict_buttons["continue"] = Button(SCREEN_WIDTH//2 - self.button_width//2, (SCREEN_HEIGHT//9) + 2*(self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[0], self.fonte_title)
        self.dict_buttons["back"] = Button(SCREEN_WIDTH//2 - self.button_width//2, (SCREEN_HEIGHT//9) + 3*(self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[1], self.fonte_title)
        
        self.dict_buttons["right1"] = Button(SCREEN_WIDTH//2 - self.button_width//2 + self.button_width +2, (SCREEN_HEIGHT//9) + 120, 25,\
                                             self.button_height, " ", self.fonte_subsubtitle, color_hover=(0, 0, 255, 0), texture_path = "./assets/game_screen/right_button.png" )
        self.dict_buttons["right2"] = Button(SCREEN_WIDTH//2 - self.button_width//2 + self.button_width +2, (SCREEN_HEIGHT//9) + (self.button_height + 10) + 120, 25,\
                                             self.button_height, " ", self.fonte_subsubtitle, color_hover=(0, 0, 255, 0), texture_path = "./assets/game_screen/right_button.png" )
        self.dict_buttons["left1"] = Button(SCREEN_WIDTH//2 - self.button_width//2 - 30, (SCREEN_HEIGHT//9) + 120, 25,\
                                             self.button_height, " ", self.fonte_subsubtitle, color_hover=(0, 0, 255, 0), texture_path = "./assets/game_screen/left_button.png" )
        self.dict_buttons["left2"] = Button(SCREEN_WIDTH//2 - self.button_width//2 - 30, (SCREEN_HEIGHT//9) + (self.button_height + 10) + 120, 25,\
                                             self.button_height, " ", self.fonte_subsubtitle, color_hover=(0, 0, 255, 0), texture_path = "./assets/game_screen/left_button.png" )
        self.loading_message = self.fonte_title_game.render("OnBeat!!", True, (255, 255, 255))
        self.index=0
        self.index_player = 0

    def resize(self, screen):
        """
        Resizes the buttons to fit the new screen size.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the buttons for.

        Notes
        -----
        The method resizes and repositions the buttons to fit the new screen size.
        The `width` and `height` attributes are used to determine the position of the buttons.
        The `button_width` and `button_height` attributes are used to determine the size of the buttons.
        """
        super().resize(screen)
        for music in self.manager.music_names:
            self.dict_buttons_music[music].rect.x = self.width//2 - self.button_width//2
            self.dict_buttons_music[music].rect.y = (self.height//9) + 120
        self.dict_buttons[self.name_player[0]].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons[self.name_player[0]].rect.y = (self.height//9) + (self.button_height + 10) + 120
        self.dict_buttons[self.name_player[1]].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons[self.name_player[1]].rect.y = (self.height//9) + (self.button_height + 10) + 120
        self.dict_buttons["continue"].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons["continue"].rect.y = (self.height//9) + 2*(self.button_height + 10) + 120
        self.dict_buttons["back"].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons["back"].rect.y = (self.height//9) + 3*(self.button_height + 10) + 120
        self.dict_buttons["right1"].rect.x = self.width//2 - self.button_width//2 + self.button_width +2
        self.dict_buttons["right1"].rect.y = (self.height//9) + 120
        self.dict_buttons["right2"].rect.x = self.width//2 - self.button_width//2 + self.button_width +2
        self.dict_buttons["right2"].rect.y = (self.height//9) + (self.button_height + 10) + 120
        self.dict_buttons["left1"].rect.x = self.width//2 - self.button_width//2 - 30
        self.dict_buttons["left1"].rect.y = (self.height//9) + 120
        self.dict_buttons["left2"].rect.x = self.width//2 - self.button_width//2 - 30
        self.dict_buttons["left2"].rect.y = (self.height//9) + (self.button_height + 10) + 120

    def draw(self, screen):
        """
        Draws the screen with the buttons and the selected music and player.
        """
        self.resize(screen)
        screen.blit(self.imagem, (0, 0))
        screen.blit(self.loading_message, (self.width//2 - self.loading_message.get_width()//2, self.height//9 + 10))
        self.dict_buttons["continue"].draw(screen)
        self.dict_buttons["back"].draw(screen)
        self.dict_buttons_music[self.manager.music_names[self.index]].draw(screen)
        self.dict_buttons[self.name_player[self.index_player]].draw(screen)
        self.dict_buttons["right1"].draw(screen)
        self.dict_buttons["right2"].draw(screen)
        self.dict_buttons["left1"].draw(screen)
        self.dict_buttons["left2"].draw(screen)
        pg.display.flip()

    def start_game(self, option):
        """
        Starts the game with the specified option.

        Parameters
        ----------
        option : int
            The option to start the game with. The options are:
                1. Start the game.
                2. Return to the main menu.

        Notes
        -----
        The method changes the state of the game based on the given option.
        """
        if option == 1:
            self.manager.change_state("game")
        if option == 2:
            self.manager.change_state("main_menu")

    def update(self, screen):
        """
        Updates the music catalog screen based on the current language and player selection.

        Parameters
        ----------
        screen : pygame.display
            The screen to update the music catalog on.

        Notes
        -----
        The button names are updated to reflect the current language settings.
        The `multiplayer` attribute of the manager is set based on the selected player index.
        """
        self.name_buttons = self.translate("music_catalog.buttons", self.manager.language)
        self.name_buttons_player = self.translate("music_catalog.player", self.manager.language)
        self.dict_buttons[self.name_player[0]].text = self.name_buttons_player[0]
        self.dict_buttons[self.name_player[1]].text = self.name_buttons_player[1]
        self.dict_buttons["continue"].text = self.name_buttons[0]
        self.dict_buttons["back"].text = self.name_buttons[1]
        if self.index_player == 0:
            self.manager.multiplayer=False
        else:
            self.manager.multiplayer=True

    def on_event(self, event:pg.event.Event,screen):
        """
        Handles events for navigating the music catalog screen.

        Parameters
        ----------
        event : pg.event.Event
            The event that occurred, typically a mouse click or key press.
        screen : pygame.display
            The screen to update the music catalog on.

        Notes
        -----
        The method checks which button is clicked and updates the current index for music names
        or player names accordingly. If the "continue" button is clicked, it sets the selected
        music and starts the game. If the "back" button is clicked, it returns to the main menu.
        """
        if self.dict_buttons["right1"].is_clicked(event):
            if self.index == len(self.manager.music_names)-1:
                    self.index = 0
            else:
                self.index += 1 
            self.draw(screen)
        if self.dict_buttons["left1"].is_clicked(event):
            if self.index == 0:
                    self.index = len(self.manager.music_names)-1
            else:
                self.index -= 1 
            self.draw(screen)
        if self.dict_buttons["left2"].is_clicked(event):
            if self.index_player == 0:
                    self.index_player = len(self.name_player)-1
            else:
                self.index_player -= 1 
            self.draw(screen)
        if self.dict_buttons["right2"].is_clicked(event):
            if self.index_player == len(self.name_player)-1:
                    self.index_player = 0
            else:
                self.index_player += 1 

        if self.dict_buttons["continue"].is_clicked(event):
            self.manager.define_music(self.index)
            self.manager.round_start()
            self.start_game(1)

        if self.dict_buttons["back"].is_clicked(event):
            self.start_game(2)
            
class Key(Screen):
    def __init__(self, keys, button_width, button_height, manager):
        """
        Initializes the Key screen.

        Parameters
        ----------
        keys : list
            A list of keys to be displayed and managed on the screen.
        button_width : int
            The width of the buttons.
        button_height : int
            The height of the buttons.
        manager : Manager
            The manager of the game.

        Notes
        -----
        This constructor initializes various attributes for the Key screen, 
        including button dimensions, translated strings, and button instances 
        for key management. It also prepares error messages and visual elements 
        for displaying the screen's title and player messages.
        """
        super().__init__(manager)
        self.button_width = button_width
        self.button_height = button_height
        self.title = self.translate("key.title", self.manager.language)
        self.error_key_in_use = self.translate("key.error_key_in_use", self.manager.language)
        self.mesage_player = self.translate("key.player", self.manager.language)
        self.name_buttons = self.translate("key.button", self.manager.language)
        self.dict_buttons= {}
        self.dict_buttons_keys = {}
        self.keys = keys
        self.previous_keys = keys.copy()
        self.error_message = None
        filepath = "./assets/notes/keyfield/"
        self.hover_color = (255, 0, 255, 50)
        self.text_color = (255,255,255)
        self.is_valid = False
        self.waiting_for_input = None
        
        for i, key in enumerate(keys):
            texture_path = filepath + f"button_{i%4}.png"
            self.dict_buttons_keys[f"button{i}"] = Button((SCREEN_WIDTH//9) + 2 * i * SCREEN_WIDTH//9, SCREEN_HEIGHT//2,SCREEN_WIDTH // 9, SCREEN_WIDTH // 9,\
                                                    pg.key.name(key), self.fonte_subtitle,self.hover_color, self.text_color, texture_path)

        self.dict_buttons["back"] = Button(SCREEN_WIDTH//2 - self.button_width//2, SCREEN_HEIGHT - self.button_height*2, self.button_width,\
                                    self.button_height,self.name_buttons[0], self.fonte_title)
        self.title_text = self.fonte_title.render(self.title[0], True, (225, 225, 225))
        self.player1 = self.fonte_title.render(self.mesage_player[0], True, (225, 225, 225))
        self.player2 = self.fonte_title.render(self.mesage_player[1], True, (225, 225, 225))
        
    def resize(self, screen):
        """
        Resizes the buttons to fit the new screen size.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the buttons for.

        Notes
        -----
        The buttons are resized and repositioned to fit the new screen size.
        The `width` and `height` attributes are used to determine the position of the buttons.
        The `button_width` and `button_height` attributes are used to determine the size of the buttons.
        """
        super().resize(screen)
        for i in range(len(self.keys)):
            self.dict_buttons_keys[f"button{i}"].rect.x = (self.width//15) + i * self.width//9
            self.dict_buttons_keys[f"button{i}"].rect.y = self.height//2
        self.dict_buttons["back"].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons["back"].rect.y =  self.height - self.button_height*2

    def start_game(self):
        """
        Starts the game with the selected keys.

        Notes
        -----
        This method is called when the "continue" button is clicked. It sets the selected
        keys on the manager and changes the state to the settings screen.
        """
        self.manager.keys = self.keys
        self.manager.change_state("settings")

    def draw_error_message(self, screen):
        """
        Draws an error message on the screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to draw the error message on.

        Notes
        -----
        The error message is drawn at the bottom of the screen, centered horizontally.
        The error message is rendered in red color.
        If the error message is None, the method does nothing.
        """
        if self.error_message:  
            error_text = self.fonte_subsubtitle.render(self.error_message, True, (255, 0, 0))
            screen.blit(error_text, (self.width//2 - error_text.get_width()//2, self.height - self.height//3))

    def draw(self,screen):
        """
        Draws the key selection screen on the given screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to draw the key selection screen on.

        Notes
        -----
        This method resizes the buttons to fit the new screen size.
        The title, player messages and keys are drawn on the screen.
        The error message is drawn at the bottom of the screen, centered horizontally.
        The error message is rendered in red color.
        If the error message is None, the method does nothing.
        """
        self.resize(screen)
        screen.blit(self.imagem, (0, 0))
        self.title_text = self.fonte_title.render(self.title[0], True, (225, 225, 225))
        screen.blit(self.title_text, (self.width//2 - self.title_text.get_width()//2, 100))
        self.player1 = self.fonte_title.render(self.mesage_player[0], True, (225, 225, 225))
        self.player2 = self.fonte_title.render(self.mesage_player[1], True, (225, 225, 225))
        screen.blit(self.player1, (self.width//6, self.height//3))
        screen.blit(self.player2, (self.width - self.width//3  - self.title_text.get_width()//8, self.height//3))
        
        for i in range(len(self.keys)):
            text_surface = self.dict_buttons_keys[f"button{i}"].font.render(self.dict_buttons_keys[f"button{i}"].text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.dict_buttons_keys[f"button{i}"].rect.center)
            self.dict_buttons_keys[f"button{i}"].draw(screen)
            screen.blit(text_surface, text_rect)
        self.dict_buttons["back"].draw(screen)
        self.draw_error_message(screen)
            
    def update(self, screen):
        """
        Updates the key screen based on the current language settings.

        Parameters
        ----------
        screen : pygame.display
            The screen to update.

        Notes
        -----
        The titles, error messages, player messages, and button names are
        translated to match the currently selected language. The back button's
        text is updated to reflect the new language settings.
        """
        self.title = self.translate("key.title", self.manager.language)
        self.error_key_in_use = self.translate("key.error_key_in_use", self.manager.language)
        self.mesage_player = self.translate("key.player", self.manager.language)
        self.name_buttons = self.translate("key.button", self.manager.language)
        self.dict_buttons["back"].text = self.name_buttons[0]

    def on_event(self, event, screen):
        """
        Handles events for the key configuration screen.

        Parameters
        ----------
        event : pygame.event.Event
            The event that occurred.
        screen : pygame.display
            The screen to update the key configuration on.

        Notes
        -----
        If a key is pressed while waiting for input, it checks if the key is not already in use.
        If not, it updates the key configuration; otherwise, it sets an error message.
        If a button is clicked, it updates the waiting_for_input index.
        If the back button is clicked, it starts the game with the current configuration.
        """
        if event.type == pg.KEYDOWN and self.waiting_for_input is not None:
            new_key = event.key
            
            if new_key not in self.keys: 
                self.keys[self.waiting_for_input] = new_key
                self.dict_buttons_keys[f"button{self.waiting_for_input}"].text = pg.key.name(new_key)
                self.previous_keys = self.keys.copy()  
                self.error_message = None
                print("Teclas atualizadas:", self.keys)
            else:
                self.error_message = self.error_key_in_use[0] + pg.key.name(new_key) + self.error_key_in_use[1]
            self.waiting_for_input = None

        for i in range(len(self.keys)):
            if self.dict_buttons_keys[f"button{i}"].is_clicked(event):
                self.waiting_for_input = i
                break

        if self.dict_buttons["back"].is_clicked(event):
            self.start_game()
            
class Game(Screen):
    def __init__(self, manager):
        """
        Initializes the Game screen.

        Parameters
        ----------
        manager : GameManager
            The manager of the game.

        Notes
        -----
        Initializes the Game screen and sets the game music settings.
        """
        pg.mixer.pre_init(44100, channels=2, buffer=512)
        pg.mixer.init()
        super().__init__(manager)
        self.needs_resize = True
        print(pg.mixer.get_init())
        self.resize = True
        self.pause = False

    def resize_background(self, screen):
        """
        Resizes the background image to fit the given screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the background image for.

        Notes
        -----
        The width and height of the screen are used to resize the background image.
        The resized image is then stored in the `imagem` attribute.
        """
        width, height = screen.get_size()
        self.imagem = pg.transform.scale(self.imagem_original, (width, height))

    def resize(self, screen):
        """
        Resizes the screen elements to fit the new screen size.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the elements for.

        Notes
        -----
        The method calls the superclass resize method to update the size of the screen elements
        and ensure they fit the new dimensions of the screen.
        """
        return super().resize(screen)

    def draw(self, screen):
        """
        Draws the game screen elements.

        Parameters
        ----------
        screen : pygame.display
            The screen to draw the game elements on.

        Notes
        -----
        This method fills the screen with a black background, resizes and draws the background image,
        iterates through each round to draw game objects, and updates the display to reflect the changes.
        """
        screen.fill((0,0,0))
        self.resize_background(screen)
        screen.blit(self.imagem, (0, 0))
        for round in self.manager.round:
            round.draw_objects(screen, self.keys)
        pg.display.flip()

    def update(self, screen):
        """
        Updates the game state for all rounds on the screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to update.

        Notes
        -----
        This method checks the state of the keys, updates the play notes for each round,
        and marks the round as not undone.
        """
        #if pg.mixer.music.get_pos() > 12000: pg.mixer.music.pause()
        for round in self.manager.round:
            round.play_notes()
        self.keys = pg.key.get_pressed()
        self.undone = False
        for round in self.manager.round:
            round.update(self.keys, screen, self.resize)

    def on_event(self,event, screen):
        """
        Handles events in the game screen.

        Parameters
        ----------
        event : pygame.event.Event
            The event that occurred.
        screen : pygame.display
            The screen to update the game elements on.

        Notes
        -----
        If the event is a key press, the method checks if the key is the escape key
        and changes the state to the main menu if it is. If the key is the "p" key,
        the method toggles the pause state of the music.
        If the event is a video resize, the method sets the resize flag to True.
        The method then calls the on_event method for each round in the game.
        """
        for round in self.manager.round:
            round.on_event(event)
        if event.type == pg.VIDEORESIZE:
            self.resize = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                for round in self.manager.round:
                    round.music.stop_music()
                self.manager.change_state("main_menu")
            if event.key == pg.K_p:
                if self.pause:
                    pg.mixer.music.unpause()  
                    self.pause = False              
                else:
                    pg.mixer.music.pause()
                    self.pause = True
class Dev(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
        """
        Initializes the developer screen.

        Parameters
        ----------
        button_width : int
            The width of the buttons.
        button_height : int
            The height of the buttons.
        manager : Manager
            The manager of the game.

        Notes
        -----
        The buttons are created and stored in the `dict_buttons` attribute.
        The `name_buttons` attribute is used to translate the button names into the selected language.
        The `dict_buttons_music` attribute is used to translate the music names into the selected language.
        The `index` attribute is used to keep track of the selected music index.
        The `loading_message` attribute is used to display the game title during the loading screen.
        """
        super().__init__(manager)
        self.button_width = button_width
        self.button_height = button_height
        self.name_buttons = self.translate("dev.buttons", self.manager.language)
        self.dict_buttons = {}
        self.dict_buttons_music= {}
        self.music_names = list(music_data.keys())
        for i,music in enumerate(self.music_names):
            music_name = music
            self.dict_buttons_music[f"music_{i}"] = Button(SCREEN_WIDTH//2 - self.button_width//2, (SCREEN_HEIGHT//9) + 120,\
                                                     self.button_width, self.button_height, music_name, self.fonte_subtitle)
        self.dict_buttons["right1"] = Button(SCREEN_WIDTH//2 - self.button_width//2 + self.button_width +2, (SCREEN_HEIGHT//9) + 120, 25,\
                                             self.button_height, " ", self.fonte_subsubtitle, color_hover=(0, 0, 255, 0), texture_path = "./assets/game_screen/right_button.png" )
        self.dict_buttons["left1"] = Button(SCREEN_WIDTH//2 - self.button_width//2 - 30, (SCREEN_HEIGHT//9) + 120, 25,\
                                             self.button_height, " ", self.fonte_subsubtitle, color_hover=(0, 0, 255, 0), texture_path = "./assets/game_screen/left_button.png" )
        self.dict_buttons["config"] = Button(SCREEN_WIDTH//2 - self.button_width//2, (SCREEN_HEIGHT//9) + (self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[0], self.fonte_title)
        self.dict_buttons["back"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + 3*(self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[1], self.fonte_title)
        self.loading_message = self.fonte_title_game.render("OnBeat!!", True, (255, 255, 255))
        self.index=0

    def resize(self, screen):
        """
        Resizes the buttons to fit the new screen size.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the buttons for.

        Notes
        -----
        The method adjusts the position of the music buttons and other UI elements
        to ensure they are centered and properly aligned according to the new screen size.
        """
        super().resize(screen)
        for i,music in enumerate(self.music_names):
            self.dict_buttons_music[f"music_{i}"].rect.x = self.width//2 - self.button_width//2
            self.dict_buttons_music[f"music_{i}"].rect.y = (self.height//9) + 120
        self.dict_buttons["config"].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons["config"].rect.y = (self.height//9) + (self.button_height + 10) + 120
        self.dict_buttons["back"].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons["back"].rect.y = (self.height//9) + 2*(self.button_height + 10) + 120
        self.dict_buttons["right1"].rect.x = self.width//2 - self.button_width//2 + self.button_width +2
        self.dict_buttons["right1"].rect.y = (self.height//9) + 120
        self.dict_buttons["left1"].rect.x = self.width//2 - self.button_width//2 - 30
        self.dict_buttons["left1"].rect.y = (self.height//9) + 120

    def draw(self, screen):
        """
        Draws the developer screen on the given screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to draw the developer screen on.

        Notes
        -----
        The method resizes the buttons to fit the new screen size.
        The method then draws the buttons and the game title on the screen.
        The method then updates the display with the new frame.
        """
        self.resize(screen)
        screen.blit(self.imagem, (0, 0))
        screen.blit(self.loading_message, (self.width//2 - self.loading_message.get_width()//2, self.height//9 + 10))
        self.dict_buttons["config"].draw(screen)
        self.dict_buttons["back"].draw(screen)
        self.dict_buttons_music[f"music_{self.index}"].draw(screen)
        self.dict_buttons["right1"].draw(screen)
        self.dict_buttons["left1"].draw(screen)
        pg.display.flip()

    def start_game(self, option):
        """
        Starts the game with the specified option.

        Parameters
        ----------
        option : int
            The option to start the game with. The options are:
                1. Start the game in developer mode.
                2. Start the game in developer mode but with the configuration screen.
                3. Return to the main menu.

        Notes
        -----
        The method changes the state of the game based on the given option.
        """
        if option == 1:
            self.manager.change_state("dev_game")
        if option == 2:
            self.manager.change_state("dev_config")
        if option == 3:
            self.manager.change_state("main_menu")

    def update(self, screen):
        """
        Updates the dev screen based on the given screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to update the dev screen on.

        Notes
        -----
        The method updates the button names based on the current language.
        """
        self.name_buttons = self.translate("dev.buttons", self.manager.language)
        self.dict_buttons["config"].text = self.name_buttons[0]
        self.dict_buttons["back"].text = self.name_buttons[1]

    def on_event(self, event, screen):
        """
        Handles events in the dev screen.

        Parameters
        ----------
        event : pygame.event.Event
            The event that occurred.
        screen : pygame.display
            The screen to update the dev screen on.

        Notes
        -----
        If the event is a mouse click, the method checks if the click was on one of the buttons.
        If the click was on a button, the method calls the start_game method with the corresponding option.
        """
        if self.dict_buttons["right1"].is_clicked(event):
            self.music_names = list(music_data.keys())
            for i,music in enumerate(self.music_names):
                music_name = music
                self.dict_buttons_music[f"music_{i}"] = Button(SCREEN_WIDTH//2 - self.button_width//2, (SCREEN_HEIGHT//9) + 120,\
                                                     self.button_width, self.button_height, music_name, self.fonte_subtitle)
            if self.index == len(self.music_names)-1:
                    self.index = 0
            else:
                self.index += 1 
            self.draw(screen)
        if self.dict_buttons["left1"].is_clicked(event):
            self.music_names = list(music_data.keys())
            for i,music in enumerate(self.music_names):
                music_name = music
                self.dict_buttons_music[f"music_{i}"] = Button(SCREEN_WIDTH//2 - self.button_width//2, (SCREEN_HEIGHT//9) + 120,\
                                                     self.button_width, self.button_height, music_name, self.fonte_subtitle)
            if self.index == 0:
                    self.index = len(self.music_names)-1
            else:
                self.index -= 1 
            self.draw(screen)
        if self.dict_buttons_music[f"music_{self.index}"].is_clicked(event):
            self.manager.dev = True
            self.manager.current_music_dev = self.dict_buttons_music[f"music_{self.index}"].text
            self.manager.round_start()
            self.start_game(1)
        if self.dict_buttons["config"].is_clicked(event):
            self.start_game(2)
        if self.dict_buttons["back"].is_clicked(event):
            self.start_game(3)
            
class DevConfg(Screen):
    
    def __init__(self, button_width:int, button_height:int, manager):
        """
        Initializes the dev config screen.

        Parameters
        ----------
        button_width : int
            The width of the buttons.
        button_height : int
            The height of the buttons.
        manager : Manager
            The manager of the game.

        Notes
        -----
        The buttons are created and stored in the `dict_buttons` attribute.
        The `name_buttons` attribute is used to translate the button names into the selected language.
        The `active_button` attribute is used to keep track of the currently active button.
        The `dict_buttons` attribute is used to store the buttons.
        The method sets the text of the buttons based on the current values of the manager's attributes.
        """
        super().__init__(manager)
        self.button_width = button_width
        self.button_height = button_height
        self.dict_buttons = {}
        self.name_buttons = self.translate("dev_config.buttons", self.manager.language)
        self.active_button = None
        self.dict_buttons["name"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) - (self.button_height + 10) + 80,\
                                             self.button_width, self.button_height, self.name_buttons[0] + f":{self.manager.name}", self.fonte_subsubtitle)
        self.dict_buttons["bpm"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + 90,\
                                             self.button_width, self.button_height, self.name_buttons[1] + f":{self.manager.bpm}", self.fonte_subsubtitle)
        self.dict_buttons["speed"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + (self.button_height + 10) + 90,\
                                             self.button_width, self.button_height, self.name_buttons[2] + f":{self.manager.speed}", self.fonte_subsubtitle)
        self.dict_buttons["path"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + 2*(self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[3] + f":{self.manager.path}", self.fonte_subsubtitle)
        self.dict_buttons["moment"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + 3*(self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[4] + f":{self.manager.moment}", self.fonte_subsubtitle)
        self.dict_buttons["back"] = Button((SCREEN_WIDTH - self.button_width)//2, (SCREEN_HEIGHT//9) + 4*(self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[5], self.fonte_title)
        self.dict_buttons["+"] = Button(SCREEN_WIDTH - 60, SCREEN_HEIGHT - 60,\
                                             50,50, self.name_buttons[6], self.fonte_title)


    def resize(self, screen):
        """
        Resizes the buttons to fit the new screen size.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the buttons for.

        Notes
        -----
        The method resizes and repositions the buttons to fit the new screen size.
        """
        super().resize(screen)
        self.dict_buttons["name"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["name"].rect.y = (self.height//9) - (self.button_height + 10) + 80
        self.dict_buttons["bpm"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["bpm"].rect.y = (self.height//9) + 80
        self.dict_buttons["speed"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["speed"].rect.y = (self.height//9) + (self.button_height + 10) + 80
        self.dict_buttons["path"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["path"].rect.y = (self.height//9) + 2*(self.button_height + 10) + 80
        self.dict_buttons["moment"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["moment"].rect.y = (self.height//9) + 3*(self.button_height + 10) + 80
        self.dict_buttons["back"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["back"].rect.y = (self.height//9) + 4*(self.button_height + 10) + 80
        self.dict_buttons["+"].rect.x = self.width - 60
        self.dict_buttons["+"].rect.y = self.height - 60

    def draw(self, screen):
        """
        Draws the buttons and the background image on the screen.

        Parameters
        ----------
        screen : pygame.display
            The screen to draw on.

        Notes
        -----
        The method first resizes the buttons to fit the new screen size.
        Then it draws the background image and the buttons on the screen.
        Finally it updates the display.
        """
        self.resize(screen)
        screen.blit(self.imagem, (0, 0))
        self.dict_buttons["name"].draw(screen)
        self.dict_buttons["bpm"].draw(screen)
        self.dict_buttons["speed"].draw(screen)
        self.dict_buttons["path"].draw(screen)
        self.dict_buttons["moment"].draw(screen)
        self.dict_buttons["back"].draw(screen)
        self.dict_buttons["+"].draw(screen)
        pg.display.flip()

    def start_game(self, option):
        """
        Starts a new game based on the given option.

        Parameters
        ----------
        option : int
            The option to start the game with. 1 for the dev screen.

        Notes
        -----
        The game state is changed to reflect the chosen option.
        """
        if option == 1:
            self.manager.change_state("dev")

    def update(self, screen):
        """
        Updates the buttons with the current values of the manager's attributes.

        Parameters
        ----------
        screen : pygame.display
            The screen to update the buttons on.

        Notes
        -----
        The method first translates the button names into the selected language.
        Then it updates the text of the buttons with the current values of the manager's attributes.
        """
        self.name_buttons = self.translate("dev_config.buttons", self.manager.language)
        self.dict_buttons["name"].text = self.name_buttons[0] + f":{self.manager.name}"
        self.dict_buttons["bpm"].text = self.name_buttons[1] + f":{self.manager.bpm}"
        self.dict_buttons["speed"].text = self.name_buttons[2] + f":{self.manager.speed}"
        self.dict_buttons["path"].text = self.name_buttons[3] + f":{self.manager.path}"
        self.dict_buttons["moment"].text = self.name_buttons[4] + f":{self.manager.moment}"
        self.dict_buttons["back"].text = self.name_buttons[5]
        self.dict_buttons["+"].text = self.name_buttons[6]

    def on_event(self, event:pg.event.Event,screen):
        """
        Handles input events on the dev config screen.

        Parameters
        ----------
        event : pg.event.Event
            The event that occurred.
        screen : pygame.display
            The screen to update the dev config on.

        Notes
        -----
        - If the '+' button is clicked, initializes a new music configuration with default values
        and writes it to 'music_test.json'.
        - Activates corresponding attribute editing when a button is clicked.
        - Updates the active attribute based on keyboard input when a key is pressed.
        - If the 'Back' button is clicked, starts the game with the dev screen.
        """
        if self.dict_buttons["+"].is_clicked(event):
            music_data[self.manager.name] = {
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
            music_data[self.manager.name]["BPM"] = int(self.manager.bpm)
            music_data[self.manager.name]["speed"] = int(self.manager.speed)
            music_data[self.manager.name]["music_file"] = self.manager.path
            music_data[self.manager.name]["file_delay"] = int(self.manager.moment)
            with open('./src/config/music_test.json', 'w') as json_file:
                json.dump(music_data, json_file)

        if self.dict_buttons["name"].is_clicked(event):
            self.active_button = "name"
        if self.dict_buttons["bpm"].is_clicked(event):
            self.active_button = "bpm"
        elif self.dict_buttons["speed"].is_clicked(event):
            self.active_button = "speed"
        elif self.dict_buttons["path"].is_clicked(event):
            self.active_button = "path"
        elif self.dict_buttons["moment"].is_clicked(event):
            self.active_button = "moment"
        elif self.dict_buttons["back"].is_clicked(event):
            self.start_game(1)

        if event.type == pg.KEYDOWN and self.active_button:
            if event.key == pg.K_BACKSPACE:
                if self.active_button == "name":
                    self.manager.name = self.manager.name[:-1]
                if self.active_button == "bpm":
                    self.manager.bpm = self.manager.bpm[:-1]
                elif self.active_button == "speed":
                    self.manager.speed = self.manager.speed[:-1]
                elif self.active_button == "path":
                    self.manager.path = self.manager.path[:-1]
                elif self.active_button == "moment":
                    self.manager.moment = self.manager.moment[:-1]
            else:
                if self.active_button == "name":
                    self.manager.name += event.unicode
                if self.active_button == "bpm":
                    self.manager.bpm += event.unicode
                elif self.active_button == "speed":
                    self.manager.speed += event.unicode
                elif self.active_button == "path":
                    self.manager.path += event.unicode
                elif self.active_button == "moment":
                    self.manager.moment += event.unicode
            self.update(screen)
            
class GameDev(Screen):
    
    def __init__(self, manager):
        """
        Initializes the GameDev screen.

        Parameters
        ----------
        manager : GameManager
            The manager of the game.

        Notes
        -----
        Initializes the GameDev screen and sets the game music settings.
        """
        pg.mixer.pre_init(44100, channels=2, buffer=512)
        pg.mixer.init()
        super().__init__(manager)
        print(pg.mixer.get_init())
        self.resize = True

    def resize_background(self, screen):
        """
        Resizes the background image to fit the given screen.

        Parameters
        ----------
        screen : pygame.Surface
            The screen to resize the background image for.

        Notes
        -----
        The width and height of the screen are used to resize the background image.
        The resized image is then stored in the `imagem` attribute.
        """
        width, height = screen.get_size()
        self.imagem = pg.transform.scale(self.imagem_original, (width, height))

    def resize(self, screen):
        """
        Resizes the buttons to fit the new screen size.

        Parameters
        ----------
        screen : pygame.display
            The screen to resize the buttons for.

        Notes
        -----
        Calls the super().resize() method to resize the buttons.
        """
        super().resize(screen)

    def draw(self, screen):
        """
        Draws the game screen elements.

        Parameters
        ----------
        screen : pygame.display
            The screen to draw the game elements on.

        Notes
        -----
        This method fills the screen with a black background, resizes and draws the background image,
        iterates through each round to draw game objects, and updates the display to reflect the changes.
        """
        screen.fill((0,0,0))
        self.resize_background(screen)
        screen.blit(self.imagem, (0, 0))
        self.manager.dev.round.draw_objects(screen, self.keys)
        self.manager.dev.draw_selection(screen, self.manager.dev.round.notes_to_play, self.manager.dev.round.music_start_pos, self.manager.dev.round.stop_index)
        self.manager.dev.draw(screen, self.manager.dev.round.music_start_pos, self.manager.dev.round.text_font)
        pg.display.flip()

    def update(self, screen):
        """
        Updates the GameDev screen state.

        Parameters
        ----------
        screen : pygame.display
            The screen to update.

        Notes
        -----
        This method handles the playback of notes, captures the current state of pressed keys, and updates
        the current round with the key states and screen information. It also ensures that the round is not marked as undone.
        """
        self.manager.dev.round.play_notes()
        self.keys = pg.key.get_pressed()
        self.undone = False
        self.manager.dev.round.update(self.keys, screen, self.resize, self.manager.dev)



    def on_event(self,event, screen):
        """
        Handles events for the GameDev screen.

        Parameters
        ----------
        event : pygame.event.Event
            The event that occurred, such as a key press or a window resize.
        screen : pygame.display
            The screen to update the elements on.

        Notes
        -----
        Delegates event handling to the dev mode. If the event is a video resize, 
        it sets the resize flag to True. If the event is a key press of the escape 
        key, it pauses the music and changes the state to the main menu.
        """
        self.manager.dev.on_event(event,[screen.get_height(), screen.get_width()])
        if event.type == pg.VIDEORESIZE:
            self.resize = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
               self.manager.dev.round.music.stop_music()
               self.manager.change_state("main_menu")


