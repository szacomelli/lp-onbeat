import pygame as pg
from threading import Timer as tm
import notes as nt, keyfields as kf, actualround as ar, music as ms
from abc import ABC, abstractmethod
import time

class Button:
    def __init__(self, x: float, y: float, width:float, height: float, text:str, font:str, color_normal:tuple, color_hover:tuple, text_color:tuple):
        self.rect = pg.Rect(x, y, width, height)
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.text = text
        self.font = font
        self.text_color = text_color
        self.hovered = False

    def draw(self, screen):
        color = self.color_hover if self.hovered else self.color_normal
        pg.draw.rect(screen, color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if event.type == pg.MOUSEMOTION:
            self.check_hover(event.pos)

        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.hovered and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                return True
            return False
    
class Screen(ABC):
    def __init__(self, size: tuple, manager):
        self.manager = manager
        self._size:tuple = size
        self._width:float = size[0]
        self._height:float = size[1]
        self.fonte_title = pg.font.Font("./assets/8bitoperator.ttf", 40)
        self.fonte_subtitle = pg.font.Font("./assets/8bitoperator.ttf", 20)

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
    def __init__(self, size:tuple, button_width:int, button_height:int, manager):
        super().__init__(size, manager)
        self.start_button = Button(self._width//2 - button_width//4+70, self._height//2, button_width,\
                                    button_height,"Start", self.fonte_title, (255,255,255),(255,25,25), (0,0,0))
        self.exit_button = Button(self._width//2 - button_width-50, self._height//2, button_width,\
                                    button_height,"Settings", self.fonte_title, (255,255,255),(255,25,25), (0,0,0))
        self.loading_message = self.fonte_title.render("OnBeat!!", True, (255, 255, 255))
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.loading_message, (self._width // 2 - self.loading_message.get_width() // 2, self._height // 2 - 100))
        self.start_button.draw(screen)
        self.exit_button.draw(screen)
        pg.display.flip()

    def start_game(self):
        self.manager.change_state("game_runner")

    def update(self):
        pass

    def on_event(self, event):
        if self.start_button.is_clicked(event):
            self.start_game()
        self.exit_button.is_clicked(event)
            
class Game(Screen):
    def __init__(self, size:tuple, manager):
        pg.mixer.pre_init(44100, channels=2, buffer=512)
        pg.mixer.init()
        super().__init__(size, manager)
        self.a = [0, 2, 7, 13]
        self.key_fields = [kf.KeyField(100, 400, (255, 0, 0), (220, 0, 0), pg.K_s),
              kf.KeyField(200, 400, (0, 255, 0), (0, 220, 0), pg.K_d), 
              kf.KeyField(300, 400, (0, 0, 255), (0, 0, 220), pg.K_k), 
              kf.KeyField(400, 400, (255, 255, 0), (220, 220, 0), pg.K_l)]
              
        self.musica = ms.ItaloMusic("./FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3", self.key_fields)
        self.round = ar.ActualRound(self.key_fields, self.musica)
        print(pg.mixer.get_init())
        self.round.start_round()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.round.draw_objects(self.keys, screen)
        pg.display.flip()

    def update(self):
        self.round.play_notes()
        self.keys = pg.key.get_pressed()
        self.undone = False
        self.round.update(self.keys)

    def on_event(self,event):
        if event.type == pg.KEYUP:
           self.round.SlowKey_held_reset(event.key)

class GameManager:
    def __init__(self):
        pg.init()
        self.SCREEN_WIDTH = 640
        self.SCREEN_HEIGHT = 480
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pg.display.set_caption("OnBeat")
        self.screen_map = {
            "main_menu": MainMenu((self.SCREEN_WIDTH,self.SCREEN_HEIGHT),250,60, self),
            "game_runner": Game((self.SCREEN_WIDTH,self.SCREEN_HEIGHT), self)
        }        
        self.current_screen = self.screen_map["main_menu"]
        self.is_running = False
        self.clock = None

    def change_state(self, screen_name):
        self.current_screen = self.screen_map[screen_name]

    def run(self):
        self.is_running = True
        self.clock = pg.time.Clock()
        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False
                self.current_screen.on_event(event)
            
            self.current_screen.update()
            self.current_screen.draw(self.screen)
            pg.display.flip() 
            self.clock.tick(60)
        pg.quit()

if __name__ == "__main__":
    app = GameManager()
    app.run()
exit()