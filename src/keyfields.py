import pygame as pg
import notes
from pathlib import Path
import os


class KeyField:
    def __init__(self, x: int, y: int, unpressed_color, pressed_color, key: int, sprite_path: str, size: int = 30):
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
        self.trian_rect = pg.Rect(x, 0, size, size)
        self.sprite_trian = MakeSprite(self.trian_rect, f"./assets/game_screen/trian/trian_{MakeSprite.identify_sprite(sprite_path)}.png")
        self.shadow_rect = pg.Rect(x, y, size, size)
        self.sprite_shadow = MakeSprite(self.shadow_rect, f"./assets/game_screen/shadow/shadow_{MakeSprite.identify_sprite(sprite_path)}.png")


    def draw(self, display):
        self.sprite_line.draw(display)
        self.sprite_shadow.draw(display)
        self.sprite_trian.draw(display)

        if self.pressed:
            self.sprite_pressed.draw(display)
        else:
            self.sprite_unpressed.draw(display)

        

    def detect_FakeNote(self, note):
        if isinstance(note, notes.FakeNote): 
            return True
        else: 
            return False

    def detect_SlowNote(self, note, combo):
        if isinstance(note, notes.SlowNote):
            if note.pressed == False: note.y_holding_start = note.rect.y
            note.pressed = True
            if note.y_holding_end - note.y_holding_start + 10*note.ratio > note.rect.height : 
                note.updating = False
                return combo + 1
            else: return combo
        else: return combo + 1
        
    def update(self, keys):
        if not keys[self.key]:
            self.pressed = False


class MakeSprite:
    def __init__(self, rect, sprite_path):
        if not pg.display.get_init():
            raise RuntimeError("O display do Pygame precisa ser inicializado antes de carregar imagens.")
        self.sprite = pg.image.load(sprite_path).convert_alpha()
        self.rect = rect

    @classmethod
    def load_sprites(cls, filepath: str) -> list:
        sprite_paths = []
        for sprite_file in Path(filepath).iterdir():
            if sprite_file.is_file():
                sprite_paths.append(str(sprite_file))  # Adiciona o caminho do arquivo
        return sorted(sprite_paths)
    @classmethod
    def identify_sprite(cls, sprite_path: str) -> str:
        nothing_extention = os.path.splitext(sprite_path)[0]
        return nothing_extention[-1]
    # @classmethod
    # def make_background(cls, screen, file_path: str, width: int, x_pos: int):
        # if not pg.display.get_init():
        #         raise RuntimeError("O display do Pygame precisa ser inicializado antes de carregar imagens.")
    #     bg_image = pg.image.load(file_path).convert_alpha() 
    #     screen_height = pg.display.get_surface().get_height()
    #     scaled_bg = pg.transform.scale(bg_image, (width, screen_height))
    #     # Define o rect para o fundo
    #     rect = pg.Rect(x_pos, 0, width, screen_height)
    #     return cls(rect, file_path)
    
    def draw(self, display):

        scaled_sprite = pg.transform.scale(self.sprite, self.rect.size)
        display.blit(scaled_sprite, self.rect.topleft)
