import pygame as pg
from threading import Timer as tm
import notes as nt, keyfields as kf, actualround as ar 


pg.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pg.time.Clock()

key_fields = [kf.KeyField(100, 400, (255, 0, 0), (220, 0, 0), pg.K_a, [0, 1, 2, 5]),
              kf.KeyField(200, 400, (0, 255, 0), (0, 220, 0), pg.K_s, [0, 1, 2, 5]), 
              kf.KeyField(300, 400, (0, 0, 255), (0, 0, 220), pg.K_d, [0, 1, 2, 5]), 
              kf.KeyField(400, 400, (255, 255, 0), (220, 220, 0), pg.K_f, [0, 1, 2, 5])]

notes_list = [nt.FastNote(key_fields[0]), nt.FastNote(key_fields[1]), nt.FastNote(key_fields[1]), nt.FastNote(key_fields[2]), nt.SlowNote(key_fields[3])]
intervals = [0, 0, 500, 0, 1000]

round = ar.ActualRound(key_fields, notes_list, intervals)
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    round.play_notes()

    screen.fill((0, 0, 0))  # clears the screen
    
    keys = pg.key.get_pressed()
    undone = False
    round.draw_objects(keys, screen)

    round.update(keys)

    pg.display.flip()  # updates the screen
    clock.tick(30)

pg.quit()