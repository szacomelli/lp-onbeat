import pygame as pg
import currentround as ar, music as ms
from screens import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class SinglePlayerGameManager:
    def __init__(self):
        pg.init()
        pg.display.set_caption("OnBeat")
        self.language = "English"
        self.screen_size = {
            "fullscreen":pg.FULLSCREEN, 
            "resize":pg.RESIZABLE
        }
        self.current_screen_size = self.screen_size["resize"]
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), self.current_screen_size)
        pg.display.set_caption("OnBeat")
        self.keys=[pg.K_s, pg.K_d, pg.K_k, pg.K_l, pg.K_x, pg.K_c, pg.K_n, pg.K_m]
        self.music_names = ["Italo Unlimited", "Tropicalia-short", "High Stakes,Low Chances"]
        self.screen_map = {
            "main_menu": MainMenu(350,60, self),
            "game": Game(self),
            "settings": Settings(250,60, self),
            "help": Help(350,60, self),
            "music_catalog": MusicCatalog(350,60, self),
            "key": Key(self.keys, 250,60, self)
        }        
        self.current_screen = self.screen_map["main_menu"]
        self.multiplayer = False
        self.is_running = False
        self.clock = None

    def define_music(self, index):
        self.music_path=[ms.ItaloMusic("./FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3", keys =[self.keys]), ms.StardewMusic("./Tropicalia - short.mp3", keys= [self.keys]), \
                         ms.StakesMusic("./FullScores/Retro Scores/Ove Melaa - High Stakes,Low Chances.mp3",keys = [self.keys])]
        self.music_path_multiplayer=[[ms.ItaloMusic("./FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3", keys =[self.keys], multiplayer= [True, 1]), ms.ItaloMusic("./FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3", keys =[[self.keys[4], self.keys[5], self.keys[6], self.keys[7]]], multiplayer= [True, 2])],\
                          [ms.StardewMusic("./Tropicalia - short.mp3", keys= [self.keys], multiplayer=[True, 1]), ms.StardewMusic("./Tropicalia - short.mp3", keys= [[self.keys[4], self.keys[5], self.keys[6], self.keys[7]]], multiplayer=[True, 2])],\
                          [ms.StakesMusic("./FullScores/Retro Scores/Ove Melaa - High Stakes,Low Chances.mp3",keys = [self.keys], multiplayer=[True,1]), ms.StakesMusic("./FullScores/Retro Scores/Ove Melaa - High Stakes,Low Chances.mp3",keys = [[self.keys[4], self.keys[5], self.keys[6], self.keys[7]]], multiplayer=[True, 2])]]
        self.current_music = self.music_path[index]
        self.current_music_multiplayer = self.music_path_multiplayer[index]

    def round_start(self):
        if not self.multiplayer:
            self.musica = self.current_music
            self.round = [ar.CurrentRound(self.musica)]
            self.round[0].start_round()
        if self.multiplayer:
            self.musica = self.current_music_multiplayer
            self.round = [ar.CurrentRound(self.musica[0]), ar.CurrentRound(self.musica[1], switch_key=pg.K_KP_ENTER)]
            self.round[0].start_round()
            self.round[1].start_round()

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
            
            self.current_screen.update(self.screen)
            self.current_screen.draw(self.screen)
            pg.display.flip() 
            self.clock.tick(60)
        pg.quit()