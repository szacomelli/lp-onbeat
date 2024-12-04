import pygame as pg
import currentround as ar, music as ms
from abc import ABC, abstractmethod
import json

with open("src/languages.json", "r", encoding="utf-8") as file:
    LANGUAGES = json.load(file)
    
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def translate(key_path, language):
    keys = key_path.split(".")
    text = LANGUAGES[language]
    for key in keys:
        text = text.get(key, None)
        if text is None:
            return key_path
    return text
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
        self.fonte_subsubtitle = pg.font.Font("./assets/8bitoperator.ttf", 10)
        self.imagem_original = pg.image.load("./assets/game_screen/fundo.png")
        self.imagem = pg.transform.scale(self.imagem_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def resize_background(self, screen):
        width, height = screen.get_size()
        self.imagem = pg.transform.scale(self.imagem_original, (width, height))

    def draw_background(self, screen):
        screen.blit(self.imagem, (0, 0))

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
        self.name_buttons = translate("main_menu.buttons", self.manager.language)
        self.dict_buttons = {}
        for i, name in enumerate(self.name_buttons):
            x = (SCREEN_WIDTH - button_width)//2
            y = (SCREEN_HEIGHT//9) + i * (button_height + 10) + 120
            self.dict_buttons[name] = Button(x, y, button_width, button_height, name, self.fonte_title)
        self.loading_message = self.fonte_title_game.render("OnBeat!!", True, (255, 255, 255))

    def draw(self, screen):
        self.resize_background(screen)
        screen.blit(self.imagem, (0, 0))
        screen.blit(self.loading_message, (SCREEN_WIDTH//2 - self.loading_message.get_width()//2, SCREEN_HEIGHT//2 - 150))
        for i in range(len(self.name_buttons)):
            self.dict_buttons[self.name_buttons[i]].draw(screen)
        pg.display.flip()

    def start_game(self, option):
        if option == 1:
            self.manager.change_state("music_catalog")
        elif option == 2:
            self.manager.change_state("settings")
        elif option == 3:
            self.manager.change_state("help")
        elif option == 4:
            self.manager.is_running = False

    def update(self, screen):
        pass

    def on_event(self, event, screen):
        for i in range(len(self.name_buttons)+1):
            if self.dict_buttons[self.name_buttons[i-1]].is_clicked(event):
                self.start_game(i)

class Help(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
        super().__init__(manager)
        self.name_button = translate("help.button", self.manager.language)
        self.back_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + (5*button_height)//3, button_width,\
                                    button_height, self.name_button[0], self.fonte_title)
        self.loading_message = self.fonte_title.render("OnBeat!!", True, (255, 255, 255))

    def draw(self, screen):
        self.resize_background(screen)
        screen.blit(self.imagem, (0, 0))
        screen.blit(self.loading_message, (SCREEN_WIDTH // 2 - self.loading_message.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        self.back_button.draw(screen)
        pg.display.flip()

    def start_game(self, option):
        if option == 1:
            self.manager.change_state("main_menu")

    def update(self, screen):
        pass

    def on_event(self, event:pg.event.Event,screen):
        if self.back_button.is_clicked(event):
            self.start_game(1)

class Settings(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
        super().__init__(manager)
        self.name_buttons = translate("settings.buttons", self.manager.language)
        self.dict_buttons = {}
        for i, name in enumerate(self.name_buttons):
            x = (SCREEN_WIDTH - button_width)//2
            y = (SCREEN_HEIGHT//9) + (i) * (button_height + 10) + 120
            self.dict_buttons[name] = Button(x, y, button_width, button_height, name, self.fonte_title)
        self.loading_message = self.fonte_title_game.render("OnBeat!!", True, (255, 255, 255))

    def draw(self, screen):
        self.resize_background(screen)
        screen.blit(self.imagem, (0, 0))
        screen.blit(self.loading_message, (SCREEN_WIDTH//2 - self.loading_message.get_width()//2, SCREEN_HEIGHT//2 - 150))
        for i in range(len(self.name_buttons)):
            self.dict_buttons[self.name_buttons[i]].draw(screen)
        pg.display.flip()

    def start_game(self, option):
        if option == 1:
            self.manager.change_state("key")
        if option == 3:
            self.manager.change_state("main_menu")

    def update(self, screen):
        pass

    def on_event(self, event, screen):
        for i in range(len(self.name_buttons)+1):
            if self.dict_buttons[self.name_buttons[i-1]].is_clicked(event):
                self.start_game(i)

class MusicCatalog(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
        super().__init__(manager)
        self.dict_buttons= {}
        for music in self.manager.music_names:
            music_name= music
            self.dict_buttons[music] = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 - button_height, button_width,\
                                    button_height,music_name, self.fonte_subtitle)
        self.continue_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + button_height//2, button_width,\
                                    button_height,"continue", self.fonte_title)
        self.back_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + (5*button_height)//3, button_width,\
                                    button_height,"Back", self.fonte_title)
        self.loading_message = self.fonte_title.render("OnBeat!!", True, (255, 255, 255))
        self.index=0

    def draw(self, screen):
        self.resize_background(screen)
        screen.blit(self.loading_message, (SCREEN_WIDTH // 2 - self.loading_message.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        self.dict_buttons[self.manager.music_names[self.index]].draw(screen)
        self.continue_button.draw(screen)
        self.back_button.draw(screen)
        pg.display.flip()

    def start_game(self, option):
        if option == 0:
            self.manager.change_state("game")
        if option == 1:
            self.manager.change_state("main_menu")

    def update(self, screen):
        pass

    def on_event(self, event:pg.event.Event,screen):
        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if keys[pg.K_RIGHT]:
                if self.index == len(self.manager.music_path)-1:
                    self.index = 0
                else:
                    self.index += 1 
                self.draw(screen)
            if keys[pg.K_LEFT]:
                if self.index == 0:
                    self.index = len(self.manager.music_path)-1
                else:
                    self.index -= 1 
                self.draw(screen)
        if self.continue_button.is_clicked(event):
            self.manager.current_music = self.manager.music_path[self.index]
            self.manager.round_start()
            self.start_game(0)
        if self.back_button.is_clicked(event):
            self.start_game(1)

class Key(Screen):
    def __init__(self, keys, button_width, button_height, manager):
        super().__init__(manager)
        self.keys = keys
        self.previous_keys = keys.copy()
        self.buttons = []
        self.error_message = None
        filepath = "./assets/notes/keyfield/"
        self.hover_color = (0, 0, 255, 50)
        self.text_color = (255,255,255)
        self.is_valid = False
        self.waiting_for_input = None
        
        for i, key in enumerate(keys):
            texture_path = filepath + f"button_{i}.png"
            pos = ((SCREEN_WIDTH // 9) + 2 * i * SCREEN_WIDTH // 9, SCREEN_HEIGHT // 2)
            button = Button(pos[0], pos[1], SCREEN_WIDTH // 9, SCREEN_WIDTH // 9, pg.key.name(key), self.fonte_subtitle,self.hover_color, self.text_color, texture_path)
            self.buttons.append(button)

        self.back_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + (5*button_height)//3, button_width,\
                                    button_height,"Back", self.fonte_title)
        
    def start_game(self):
        self.manager.change_state("settings")

    def draw_error_message(self, screen):
        if self.error_message:  
            error_text = self.fonte_subsubtitle.render(self.error_message, True, (255, 0, 0))
            screen.blit(error_text, (SCREEN_WIDTH // 2 - error_text.get_width() // 2, SCREEN_HEIGHT - 50))

    def draw(self,screen):
        self.resize_background(screen)
        screen.blit(self.imagem, (0, 0))
        title_text = self.fonte_subtitle.render("Configuração das teclas:", True, (225, 225, 225))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        for i, button in enumerate(self.buttons):
            text_surface = button.font.render(button.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=button.rect.center)
            button.draw(screen)
            screen.blit(text_surface, text_rect)

        self.back_button.draw(screen)
        self.draw_error_message(screen)
            
    def update(self, screen):
        pass

    def on_event(self, event, screen):
        if event.type == pg.KEYDOWN and self.waiting_for_input is not None:
            new_key = event.key
            
            if new_key not in self.keys: 
                self.keys[self.waiting_for_input] = new_key
                self.buttons[self.waiting_for_input].text = pg.key.name(new_key)
                self.previous_keys = self.keys.copy()  
                self.error_message = None
                print("Teclas atualizadas:", self.keys)
            else:
                self.error_message = f"A tecla '{pg.key.name(new_key)}' já está em uso. Escolha outra tecla."
            self.waiting_for_input = None

        elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEMOTION:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event):
                    self.waiting_for_input = i
                    break

        if self.back_button.is_clicked(event):
            self.start_game()

class Game(Screen):
    def __init__(self, manager):
        pg.mixer.pre_init(44100, channels=2, buffer=512)
        pg.mixer.init()
        super().__init__(manager)
        self.needs_resize = True
        print(pg.mixer.get_init())
        # self.resize = False

    def resize_background(self, screen):
        width, height = screen.get_size()
        self.imagem = pg.transform.scale(self.imagem_original, (width, height))

    def draw(self, screen):
        screen.fill((0,0,0))

        self.resize_background(screen) 
        screen.blit(self.imagem, (0, 0))

        self.manager.round.draw_objects(screen, self.keys)
        pg.display.flip()

    def update(self, screen):
        #if pg.mixer.music.get_pos() > 12000: pg.mixer.music.pause()
        self.manager.round.play_notes()
        self.keys = pg.key.get_pressed()
        self.undone = False
        self.manager.round.update(self.keys, screen, self.needs_resize)
        # self.resize = False

    def on_event(self,event, screen):
        self.manager.round.on_event(event)
        if event.type == pg.VIDEORESIZE:
            self.resize = True

class GameManager:
    def __init__(self):
        pg.init()
        pg.display.set_caption("OnBeat")

        self.languages = ["English", "pt/br"]
        self.language = self.languages[1]
        
        self.screen_size = {
            "fullscreen":pg.FULLSCREEN, 
            "resize":pg.RESIZABLE
        }
        self.current_screen_size = self.screen_size["resize"]
        
        flags = pg.OPENGL | pg.FULLSCREEN
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), self.current_screen_size,   vsync=1)
        pg.display.set_caption("OnBeat")
        self.keys=[pg.K_s, pg.K_d, pg.K_k, pg.K_l]
        self.music_names = ["Italo Unlimited", "Tropicalia-short", "High Stakes,Low Chances"]
        self.music_path=[ms.ItaloMusic("./FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3", keys =[self.keys]), ms.StardewMusic("./Tropicalia - short.mp3", keys= [self.keys]), \
                         ms.StakesMusic("./FullScores/Retro Scores/Ove Melaa - High Stakes,Low Chances.mp3",keys = [self.keys])]
        self.current_music= self.music_path[0]
        self.screen_map = {
            "main_menu": MainMenu(350,60, self),
            "game": Game(self),
            "settings": Settings(250,60, self),
            "help": Help(350,60, self),
            "music_catalog": MusicCatalog(350,60, self),
            "key": Key(self.keys, 250,60, self)
        }        
        self.current_screen = self.screen_map["main_menu"]
        self.is_running = False
        self.clock = None

    def round_start(self):
        self.a = [0, 2, 7, 13]
        self.musica = self.current_music
        self.round = ar.CurrentRound(self.musica)
        self.round.start_round()

    def change_state(self, screen_name):
        self.current_screen = self.screen_map[screen_name]
        self.current_screen.resize_background(self.screen)

    def run(self):
        self.is_running = True
        self.clock = pg.time.Clock()
        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False
                elif event.type == pg.VIDEORESIZE:
                    self.screen = pg.display.set_mode(event.size, self.current_screen_size)
                    self.current_screen.resize_background(self.screen)
                    self.current_screen.on_event(event, self.screen)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_F11:
                        if self.current_screen_size == self.screen_size["resize"]:
                            self.current_screen_size = self.screen_size["fullscreen"]
                            self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), self.current_screen_size)
                        else:
                            self.current_screen_size = self.screen_size["resize"]
                            self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), self.current_screen_size)
                self.current_screen.on_event(event,self.screen)

            self.current_screen.update(self.screen)
            self.current_screen.draw(self.screen)
            pg.display.flip() 
            self.clock.tick(60)
        pg.quit()

if __name__ == "__main__":
    app = GameManager()
    app.run()
exit()