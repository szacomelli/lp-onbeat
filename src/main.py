import pygame as pg
from threading import Timer as tm
import notes as nt, keyfields as kf, currentround as cr, music as ms, playground as pgr

pg.mixer.pre_init(44100, channels=2, buffer=512)
pg.mixer.init()
pg.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)



clock = pg.time.Clock()
# a = [0, 2, 7, 13]
# key_fields = [kf.KeyField(100, 400, (255, 0, 0), (220, 0, 0), pg.K_s),
#               kf.KeyField(200, 400, (0, 255, 0), (0, 220, 0), pg.K_d), 
#               kf.KeyField(300, 400, (0, 0, 255), (0, 0, 220), pg.K_k), 
#               kf.KeyField(400, 400, (255, 255, 0), (220, 220, 0), pg.K_l)]

playground = pgr.Playground(220,50,200,480,keys=[pg.K_d,pg.K_f,pg.K_j,pg.K_k])

musica = ms.StardewMusic("./Tropicalia-short.mp3", playground.key_fields)
#musica = ms.ItaloMusic("./FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3", playground.key_fields)
round = cr.CurrentRound(playground.key_fields, musica, playground)

 #+ notes_refrao.copy() + notes_refrao.copy() + notes_refrao.copy()

round.start_round()

print(pg.mixer.get_init())

screen_size = [480,640]

running = True
resize = False
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYUP:
            round.SlowKey_held_reset(event.key)
        if event.type == pg.VIDEORESIZE:
            resize = True

    round.play_notes()
    
    screen.fill((0, 0, 0))  # clears the screen
    
    

    keys = pg.key.get_pressed()
    undone = False
    round.draw_objects(keys, screen)


    resize = round.update(keys,screen,resize)

    pg.display.flip()  # updates the screen
    clock.tick(60)

pg.quit()