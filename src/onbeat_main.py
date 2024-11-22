import pygame as pg
from threading import Timer as tm
import notes as nt, keyfields as kf, actualround as ar, music as ms
from abc import ABC, abstractmethod
import time
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class Button:
    def __init__(self, x: float, y: float, width:float, height: float, text:str, font:str, color_hover = (255,25,25), text_color = (0,0,0), texture_path: str=None):
        self.rect = pg.Rect(x, y, width, height)
        self.color_normal = (255,255,255)
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

        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.hovered and event.button == 1:
                #pg.mixer.Sound('./assets/sounds/menu_select.wav').play()
                return True
            return False
    
class Screen(ABC):
    def __init__(self, manager):
        self.manager = manager
        self.fonte_title = pg.font.Font("../assets/8bitoperator.ttf", 40)
        self.fonte_subtitle = pg.font.Font("../assets/8bitoperator.ttf", 20)
        self.fonte_subsubtitle = pg.font.Font("../assets/8bitoperator.ttf", 10)

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def on_event(self):
        pass

class MainMenu(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
        super().__init__(manager)
        self.start_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 - button_height, button_width,\
                                    button_height,"Start", self.fonte_title)
        self.settings_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + button_height//3, button_width,\
                                    button_height,"Settings", self.fonte_title)
        self.help_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + (5*button_height)//3 -5, button_width,\
                                    button_height,"Help", self.fonte_title)
        self.exit_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + (9*button_height)//3 - 10, button_width,\
                                    button_height,"Exit", self.fonte_title)
        self.loading_message = self.fonte_title.render("OnBeat!!", True, (255, 255, 255))
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.loading_message, (SCREEN_WIDTH // 2 - self.loading_message.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        self.start_button.draw(screen)
        self.settings_button.draw(screen)
        self.help_button.draw(screen)
        self.exit_button.draw(screen)
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
    def update(self):
        pass

    def on_event(self, event, screen):
        if self.start_button.is_clicked(event):
            self.start_game(1)
        elif self.settings_button.is_clicked(event):
            self.start_game(2)
        elif self.help_button.is_clicked(event):
            self.start_game(3)
        elif self.exit_button.is_clicked(event):
            self.start_game(4)

class Help(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
        super().__init__(manager)
        self.back_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + (5*button_height)//3, button_width,\
                                    button_height,"Back", self.fonte_title)
        self.loading_message = self.fonte_title.render("OnBeat!!", True, (255, 255, 255))
    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.loading_message, (SCREEN_WIDTH // 2 - self.loading_message.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        self.back_button.draw(screen)
        pg.display.flip()

    def start_game(self, option):
        if option == 1:
            self.manager.change_state("main_menu")

    def update(self):
        pass

    def on_event(self, event:pg.event.Event,screen):
        if self.back_button.is_clicked(event):
            self.start_game(1)

class Settings(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
        super().__init__(manager)
        self.keys = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 - button_height, button_width,\
                                    button_height,"Keys", self.fonte_title)
        self.deley = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + button_height//3, button_width,\
                                    button_height,"Delay", self.fonte_title)
        self.back_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + (5*button_height)//3, button_width,\
                                    button_height,"Back", self.fonte_title)
        self.loading_message = self.fonte_title.render("OnBeat!!", True, (255, 255, 255))

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.loading_message, (SCREEN_WIDTH // 2 - self.loading_message.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        self.keys.draw(screen)
        self.deley.draw(screen)
        self.back_button.draw(screen)
        pg.display.flip()

    def start_game(self, option):
        if option == 1:
            self.manager.change_state("key")
        if option == 3:
            self.manager.change_state("main_menu")

    def update(self):
        pass

    def on_event(self, event, screen):
        if self.keys.is_clicked(event):
            self.start_game(1)
        elif self.deley.is_clicked(event):
            self.start_game(2)
        elif self.back_button.is_clicked(event):
            self.start_game(3)

class MusicCatalog(Screen):
    def __init__(self, button_width:int, button_height:int, manager):
        super().__init__(manager)
        self.dict_buttons= {}
        for music in self.manager.music_path:
            music_name=(music.split(" - ")[1]).split(".")[0]
            self.dict_buttons[music] = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 - button_height, button_width,\
                                    button_height,music_name, self.fonte_subtitle)
        self.continue_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + button_height//2, button_width,\
                                    button_height,"continue", self.fonte_title)
        self.back_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + (5*button_height)//3, button_width,\
                                    button_height,"Back", self.fonte_title)
        self.loading_message = self.fonte_title.render("OnBeat!!", True, (255, 255, 255))
        self.index=0
    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.loading_message, (SCREEN_WIDTH // 2 - self.loading_message.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        self.dict_buttons[self.manager.music_path[self.index]].draw(screen)
        self.continue_button.draw(screen)
        self.back_button.draw(screen)
        pg.display.flip()

    def start_game(self, option):
        if option == 0:
            self.manager.change_state("game")
        if option == 1:
            self.manager.change_state("main_menu")

    def update(self):
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
        filepath = "../assets/notes/keyfield/"
        self.hover_color = (0, 0, 255, 50)
        self.text_color = (255,255,255)
        self.is_valid = False
        self.waiting_for_input = None
        
        for i, key in enumerate(keys):
            texture_path = filepath + f"botao_{i}.png"
            pos = ((SCREEN_WIDTH // 9) + 2 * i * SCREEN_WIDTH // 9, SCREEN_HEIGHT // 2)
            button = Button(pos[0], pos[1], SCREEN_WIDTH // 9, SCREEN_WIDTH // 9, pg.key.name(key), self.fonte_subtitle,self.hover_color, self.text_color, texture_path)
            self.buttons.append(button)

        self.back_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT//2 + (5*button_height)//3, button_width,\
                                    button_height,"Back", self.fonte_title)
        
    def start_game(self):
        self.manager.change_state("main_menu")

    def draw_error_message(self, screen):
        if self.error_message:  
            error_text = self.fonte_subsubtitle.render(self.error_message, True, (255, 0, 0))
            screen.blit(error_text, (SCREEN_WIDTH // 2 - error_text.get_width() // 2, SCREEN_HEIGHT - 50))

    def draw(self,screen):
        screen.fill((0, 0, 0))
        title_text = self.fonte_subtitle.render("Configuração das teclas:", True, (225, 225, 225))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        for i, button in enumerate(self.buttons):
            text_surface = button.font.render(button.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=button.rect.center)
            button.draw(screen)
            screen.blit(text_surface, text_rect)

        self.back_button.draw(screen)
        self.draw_error_message(screen)
            
    def update(self):
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
        print(pg.mixer.get_init())

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.manager.round.draw_objects(self.keys, screen)
        pg.display.flip()

    def update(self):
        #if pg.mixer.music.get_pos() > 12000: pg.mixer.music.pause()
        self.manager.round.play_notes()
        self.keys = pg.key.get_pressed()
        self.undone = False
        self.manager.round.update(self.keys)

    def on_event(self,event, screen):
        if event.type == pg.KEYUP:
           self.manager.round.SlowKey_held_reset(event.key)

class GameManager:
    def __init__(self):
        pg.init()
        self.screen_size = {
            "fullscreen":pg.FULLSCREEN, 
            "resize":pg.RESIZABLE
        }
        self.current_screen_size = self.screen_size["resize"]
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), self.current_screen_size)
        pg.display.set_caption("OnBeat")
        self.music_path=["../FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3", "../FullScores/Retro Scores/Ove Melaa - Italo Unlimited2.mp3","../FullScores/Retro Scores/Ove Melaa - Italo Unlimited3.mp3"]
        self.current_music= self.music_path[0]
        self.keys=[pg.K_s, pg.K_d, pg.K_k, pg.K_l]
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
        self.key_fields = [kf.KeyField(100, 400, (255, 0, 0), (220, 0, 0), self.keys[0]),
              kf.KeyField(200, 400, (0, 255, 0), (0, 220, 0), self.keys[1]), 
              kf.KeyField(300, 400, (0, 0, 255), (0, 0, 220), self.keys[2]), 
              kf.KeyField(400, 400, (255, 255, 0), (220, 220, 0), self.keys[3])]
        print(self.current_music)
        self.musica = ms.ItaloMusic(self.current_music, self.key_fields)
        self.round = ar.ActualRound(self.key_fields, self.musica)
        self.round.start_round()

    def change_state(self, screen_name):
        self.current_screen = self.screen_map[screen_name]

    def run(self):
        self.is_running = True
        self.clock = pg.time.Clock()
        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_F11:
                        if self.current_screen_size == self.screen_size["resize"]:
                            self.current_screen_size = self.screen_size["fullscreen"]
                            self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), self.current_screen_size)
                        else:
                            self.current_screen_size = self.screen_size["resize"]
                            self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), self.current_screen_size)
                self.current_screen.on_event(event,self.screen)
            
            self.current_screen.update()
            self.current_screen.draw(self.screen)
            pg.display.flip() 
            self.clock.tick(60)
        pg.quit()

if __name__ == "__main__":
    app = GameManager()
    app.run()
exit()