import pygame as pg
import os
from pathlib import Path

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def CreateSprites(filepath: str) -> list:
    sprites = []
    for sprite in Path(filepath).iterdir():
        if sprite.is_file():
            sprites.append(pg.image.load(str(sprite)))
    return sprites

class KeyField:
    def __init__(self, x: int, y: int, key: int, sprite: pg.Surface, size: int = 50):
        self.size = size
        self.rect = pg.Rect(x, y, self.size, self.size)
        self.key = key
        self.pressed = False
        self.sprite = sprite
        self.sprite = pg.transform.scale(self.sprite, (self.size, self.size))
        self.make_sprite = MakeSprites(x, y, self.size, self.size, self.sprite)

    def draw(self, display):
        self.make_sprite.draw(display)

        # if self.pressed:
        #     pg.draw.rect(display, (255, 0, 0), self.rect, width=3)  # Borda vermelha se pressionado
        # else:
        #     pg.draw.rect(display, (0, 255, 0), self.rect, width=3)  # Borda verde se não pressionado

    def update(self, keys):
        self.pressed = keys[self.key]  # Verifica se a tecla específica está pressionada

class MakeSprites(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, sprite: pg.Surface):
        pg.sprite.Sprite.__init__(self)
        self.sprite = sprite
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, display):
        display.blit(self.sprite, (self.x, self.y))

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("KeyField Test")
clock = pg.time.Clock()

filepath = "./assets/notes/keyfield/"
sprites = CreateSprites(filepath)

keyfields = [
    KeyField(100, 100, pg.K_a, sprites[0], size=50),
    KeyField(200, 100, pg.K_s, sprites[1], size=50),
    KeyField(300, 100, pg.K_d, sprites[2], size=50),
    KeyField(400, 100, pg.K_f, sprites[3], size=50),
    KeyField(500, 100, pg.K_f, sprites[3], size=50),
]

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    keys = pg.key.get_pressed()

    for keyfield in keyfields:
        keyfield.update(keys)
        keyfield.draw(screen)

    pg.display.flip()
    clock.tick(60)
pg.quit()
