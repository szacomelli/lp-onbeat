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
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if event.type == pg.MOUSEMOTION:
            self.__check_hover(event.pos)
            return False
        elif event.type == pg.MOUSEBUTTONDOWN and self.hovered and event.button == 1:
            return True
        return False
class Screen(ABC):
    def __init__(self, manager):
        self.manager = manager
        self.fonte_title_game = pg.font.Font("./assets/8bitoperator.ttf", 45)       
        self.fonte_title = pg.font.Font("./assets/8bitoperator.ttf", 35)
        self.fonte_subtitle = pg.font.Font("./assets/8bitoperator.ttf", 20)
        self.fonte_subsubtitle = pg.font.Font("./assets/8bitoperator.ttf", 17)
        self.imagem_original = pg.image.load("./assets/game_screen/fundo.png")
        self.imagem = pg.transform.scale(self.imagem_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def translate(self, key_path, language):
        keys = key_path.split(".")
        text = LANGUAGES[language]
        for key in keys:
            text = text.get(key, None)
            if text is None:
                return key_path
        return text

    @abstractmethod
    def resize(self, screen):
        self.width, self.height = screen.get_size()
        self.imagem = pg.transform.scale(self.imagem_original, (self.width, self.height))

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def update(self, screen):
        pass

    @abstractmethod
    def on_event(self, screen):
        pass
class MainMenu(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
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
        self.name_buttons = self.translate("main_menu.buttons", self.manager.language)
        self.dict_buttons["start"].text = self.name_buttons[0]
        self.dict_buttons["settings"].text = self.name_buttons[1]
        self.dict_buttons["ModDev"].text = self.name_buttons[2]
        self.dict_buttons["Help"].text = self.name_buttons[3]
        self.dict_buttons["Exit"].text = self.name_buttons[4]

    def on_event(self, event, screen):
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
        super().__init__(manager)
        self.button_width = button_width
        self.button_height = button_height
        self.dict_buttons = {}
        self.name_button = self.translate("help.button", self.manager.language)
        self.dict_buttons["back"]= Button(SCREEN_WIDTH//2 - self.button_width//2, SCREEN_HEIGHT - self.button_height//3,\
                                           self.button_width, self.button_height, self.name_button[0], self.fonte_title)
        self.loading_message = self.fonte_title_game.render("OnBeat!!", True, (255, 255, 255))

    def resize(self, screen):
        super().resize(screen)
        self.dict_buttons["back"].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons["back"].rect.y = self.height - (5*self.button_height)//3

    def draw(self, screen):
        self.resize(screen)
        screen.blit(self.imagem, (0, 0))
        screen.blit(self.loading_message, (self.width//2 - self.loading_message.get_width()//2, self.height//9 + 10))
        self.dict_buttons["back"].draw(screen)
        pg.display.flip()

    def start_game(self, option):
        if option == 1:
            self.manager.change_state("main_menu")

    def update(self, screen):
        self.name_buttons = self.translate("help.button", self.manager.language)
        self.dict_buttons["back"].text = self.name_buttons[0]

    def on_event(self, event:pg.event.Event,screen):
        if self.dict_buttons["back"].is_clicked(event):
            self.start_game(1)
class Settings(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
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
        super().resize(screen)
        self.dict_buttons["language"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["language"].rect.y = (self.height//9) + 120
        self.dict_buttons["keys"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["keys"].rect.y = (self.height//9) + (self.button_height + 10) + 120
        self.dict_buttons["back"].rect.x = (self.width - self.button_width)//2
        self.dict_buttons["back"].rect.y = (self.height//9) + 2*(self.button_height + 10) + 120

    def draw(self, screen):
        self.resize(screen)
        screen.blit(self.imagem, (0, 0))
        screen.blit(self.loading_message, (self.width//2 - self.loading_message.get_width()//2, self.height//9 + 10))
        self.dict_buttons["language"].draw(screen)
        self.dict_buttons["keys"].draw(screen)
        self.dict_buttons["back"].draw(screen)
        pg.display.flip()

    def start_game(self, option):
        if option == 1:
            self.manager.language = "English" if self.manager.language == "pt/br" else "pt/br"
        if option == 2:
            self.manager.change_state("key")
        if option == 3:
            self.manager.change_state("main_menu")

    def update(self, screen):
        self.name_buttons = self.translate("settings.buttons", self.manager.language)
        self.dict_buttons["language"].text = self.name_buttons[0]
        self.dict_buttons["keys"].text = self.name_buttons[1]
        self.dict_buttons["back"].text = self.name_buttons[2]

    def on_event(self, event, screen):
        if self.dict_buttons["language"].is_clicked(event):
            self.start_game(1)
        if self.dict_buttons["keys"].is_clicked(event):
            self.start_game(2)
        if self.dict_buttons["back"].is_clicked(event):
            self.start_game(3)
class MusicCatalog(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
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
        self.dict_buttons["back"] = Button(SCREEN_WIDTH//2 - self.button_width//2, (SCREEN_HEIGHT//9) + 2*(self.button_height + 10) + 120,\
                                             self.button_width, self.button_height, self.name_buttons[0], self.fonte_title)
        
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
        super().resize(screen)
        for music in self.manager.music_names:
            self.dict_buttons_music[music].rect.x = self.width//2 - self.button_width//2
            self.dict_buttons_music[music].rect.y = (self.height//9) + 120
        self.dict_buttons[self.name_player[0]].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons[self.name_player[0]].rect.y = (self.height//9) + (self.button_height + 10) + 120
        self.dict_buttons[self.name_player[1]].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons[self.name_player[1]].rect.y = (self.height//9) + (self.button_height + 10) + 120
        self.dict_buttons["back"].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons["back"].rect.y = (self.height//9) + 2*(self.button_height + 10) + 120
        self.dict_buttons["right1"].rect.x = self.width//2 - self.button_width//2 + self.button_width +2
        self.dict_buttons["right1"].rect.y = (self.height//9) + 120
        self.dict_buttons["right2"].rect.x = self.width//2 - self.button_width//2 + self.button_width +2
        self.dict_buttons["right2"].rect.y = (self.height//9) + (self.button_height + 10) + 120
        self.dict_buttons["left1"].rect.x = self.width//2 - self.button_width//2 - 30
        self.dict_buttons["left1"].rect.y = (self.height//9) + 120
        self.dict_buttons["left2"].rect.x = self.width//2 - self.button_width//2 - 30
        self.dict_buttons["left2"].rect.y = (self.height//9) + (self.button_height + 10) + 120

    def draw(self, screen):
        self.resize(screen)
        screen.fill((0,0,0))
        screen.blit(self.imagem, (0, 0))
        screen.blit(self.loading_message, (self.width//2 - self.loading_message.get_width()//2, self.height//9 + 10))
        self.dict_buttons[self.name_player[self.index_player]].draw(screen)
        self.dict_buttons["back"].draw(screen)
        self.dict_buttons_music[self.manager.music_names[self.index]].draw(screen)
        self.dict_buttons["right1"].draw(screen)
        self.dict_buttons["right2"].draw(screen)
        self.dict_buttons["left1"].draw(screen)
        self.dict_buttons["left2"].draw(screen)
        pg.display.flip()

    def start_game(self, option):
        if option == 1:
            self.manager.change_state("game")
        if option == 2:
            self.manager.change_state("main_menu")

    def update(self, screen):
        self.name_buttons = self.translate("music_catalog.buttons", self.manager.language)
        self.name_buttons_player = self.translate("music_catalog.player", self.manager.language)
        self.dict_buttons[self.name_player[0]].text = self.name_buttons_player[0]
        self.dict_buttons[self.name_player[1]].text = self.name_buttons_player[1]
        self.dict_buttons["back"].text = self.name_buttons[0]

    def on_event(self, event:pg.event.Event,screen):
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
        if self.dict_buttons[self.name_player[0]].is_clicked(event):
            self.manager.multiplayer = False
            self.manager.define_music(self.index)
            self.manager.round_start()
            self.start_game(1)

        if self.dict_buttons[self.name_player[1]].is_clicked(event):
            self.manager.multiplayer = True
            self.manager.define_music(self.index)
            self.manager.round_start()
            self.start_game(1)

        if self.dict_buttons["back"].is_clicked(event):
            self.start_game(2)
class Key(Screen):
    def __init__(self, keys, button_width, button_height, manager):
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
        super().resize(screen)
        for i in range(len(self.keys)):
            self.dict_buttons_keys[f"button{i}"].rect.x = (self.width//15) + i * self.width//9
            self.dict_buttons_keys[f"button{i}"].rect.y = self.height//2
        self.dict_buttons["back"].rect.x = self.width//2 - self.button_width//2
        self.dict_buttons["back"].rect.y =  self.height - self.button_height*2

    def start_game(self):
        self.manager.keys = self.keys
        self.manager.change_state("settings")

    def draw_error_message(self, screen):
        if self.error_message:  
            error_text = self.fonte_subsubtitle.render(self.error_message, True, (255, 0, 0))
            screen.blit(error_text, (self.width//2 - error_text.get_width()//2, self.height - self.height//3))

    def draw(self,screen):
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
        self.title = self.translate("key.title", self.manager.language)
        self.error_key_in_use = self.translate("key.error_key_in_use", self.manager.language)
        self.mesage_player = self.translate("key.player", self.manager.language)
        self.name_buttons = self.translate("key.button", self.manager.language)
        self.dict_buttons["back"].text = self.name_buttons[0]

    def on_event(self, event, screen):
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
        pg.mixer.pre_init(44100, channels=2, buffer=512)
        pg.mixer.init()
        super().__init__(manager)
        self.needs_resize = True
        print(pg.mixer.get_init())
        self.resize = True

    def resize_background(self, screen):
        width, height = screen.get_size()
        self.imagem = pg.transform.scale(self.imagem_original, (width, height))

    def resize_background(self, screen):
        width, height = screen.get_size()
        self.imagem = pg.transform.scale(self.imagem_original, (width, height))
    def resize(self, screen):
        return super().resize(screen)

    def draw(self, screen):
        screen.fill((0,0,0))
        self.resize_background(screen)
        screen.blit(self.imagem, (0, 0))
        for round in self.manager.round:
            round.draw_objects(screen, self.keys)
        pg.display.flip()

    def update(self, screen):
        #if pg.mixer.music.get_pos() > 12000: pg.mixer.music.pause()
        for round in self.manager.round:
            round.play_notes()
        self.keys = pg.key.get_pressed()
        self.undone = False
        for round in self.manager.round:
            round.update(self.keys, screen, self.resize)

    def on_event(self,event, screen):
        for round in self.manager.round:
            round.on_event(event)
        if event.type == pg.VIDEORESIZE:
            self.resize = True
class Dev(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
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
        if option == 1:
            self.manager.change_state("dev_game")
        if option == 2:
            self.manager.change_state("dev_config")
        if option == 3:
            self.manager.change_state("main_menu")

    def update(self, screen):
        self.name_buttons = self.translate("dev.buttons", self.manager.language)
        self.dict_buttons["config"].text = self.name_buttons[0]
        self.dict_buttons["back"].text = self.name_buttons[1]

    def on_event(self, event, screen):
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
        if option == 1:
            self.manager.change_state("dev")

    def update(self, screen):
        self.name_buttons = self.translate("dev_config.buttons", self.manager.language)
        self.dict_buttons["name"].text = self.name_buttons[0] + f":{self.manager.name}"
        self.dict_buttons["bpm"].text = self.name_buttons[1] + f":{self.manager.bpm}"
        self.dict_buttons["speed"].text = self.name_buttons[2] + f":{self.manager.speed}"
        self.dict_buttons["path"].text = self.name_buttons[3] + f":{self.manager.path}"
        self.dict_buttons["moment"].text = self.name_buttons[4] + f":{self.manager.moment}"
        self.dict_buttons["back"].text = self.name_buttons[5]
        self.dict_buttons["+"].text = self.name_buttons[6]

    def on_event(self, event:pg.event.Event,screen):
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
        pg.mixer.pre_init(44100, channels=2, buffer=512)
        pg.mixer.init()
        super().__init__(manager)
        print(pg.mixer.get_init())
        self.resize = True

    def resize_background(self, screen):
        width, height = screen.get_size()
        self.imagem = pg.transform.scale(self.imagem_original, (width, height))

    def resize(self, screen):
        super().resize(screen)

    def draw(self, screen):
        screen.fill((0,0,0))
        self.resize_background(screen)
        screen.blit(self.imagem, (0, 0))
        self.dev.round.draw_objects(screen, self.keys)
        self.dev.draw_selection(screen, self.manager.dev.round.notes_to_play, self.manager.dev.round.music_start_pos, self.manager.dev.round.stop_index)
        self.dev.draw(screen, self.manager.dev.round.music_start_pos, self.manager.dev.round.text_font)
        pg.display.flip()

    def update(self, screen):
        #if pg.mixer.music.get_pos() > 12000: pg.mixer.music.pause()
        self.manager.dev.round.play_notes()
        self.keys = pg.key.get_pressed()
        self.undone = False
        self.manager.dev.round.update(self.keys, screen, self.resize)

    def on_event(self,event, screen):
        self.manager.dev.on_event(event)
        if event.type == pg.VIDEORESIZE:
            self.resize = True