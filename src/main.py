import pygame as pg
from threading import Timer as tm
import notes as nt, keyfields as kf, actualround as ar, music as ms
import screen_classes as sc

pg.mixer.pre_init(44100, channels=2, buffer=512)
pg.mixer.init()
pg.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



clock = pg.time.Clock()
a = [0, 2, 7, 13]
key_fields = [kf.KeyField(100, 400, (255, 0, 0), (220, 0, 0), pg.K_s),
              kf.KeyField(200, 400, (0, 255, 0), (0, 220, 0), pg.K_d), 
              kf.KeyField(300, 400, (0, 0, 255), (0, 0, 220), pg.K_k), 
              kf.KeyField(400, 400, (255, 255, 0), (220, 220, 0), pg.K_l)]


musica = ms.ItaloMusic("./FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3", key_fields)
round = ar.ActualRound(key_fields, musica)

 #+ notes_refrao.copy() + notes_refrao.copy() + notes_refrao.copy()

round.start_round()

print(pg.mixer.get_init())


running = True
running = sc.Welcome_screen((SCREEN_WIDTH,SCREEN_HEIGHT),running, clock).run()
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYUP:
            round.SlowKey_held_reset(event.key)

    round.play_notes()

    screen.fill((0, 0, 0))  # clears the screen
    
    keys = pg.key.get_pressed()
    undone = False
    round.draw_objects(keys, screen)


    round.update(keys)

    pg.display.flip()  # updates the screen
    clock.tick(60)

pg.quit()