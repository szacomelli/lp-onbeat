import pygame as pg
import currentround as cr, music as ms, playground as pgr

pg.mixer.pre_init(44100, channels=2, buffer=512)
pg.mixer.init()
pg.init()

screen_size = [480,640]
screen = pg.display.set_mode((screen_size[1], screen_size[0]), pg.RESIZABLE)

clock = pg.time.Clock()

playground = pgr.Playground(184,50,275,480,keys=[pg.K_d,pg.K_f,pg.K_j,pg.K_k], blank_space_percentage=0.20)

#musica = ms.StardewMusic("./Tropicalia-short.mp3", playground.key_fields)
musica = ms.ItaloMusic("./FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3", playground.key_fields)
round = cr.CurrentRound(playground.key_fields, musica, playground, speed=musica.speed)

round.start_round()

running = True
resize = False
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.VIDEORESIZE:
            resize = True

    round.play_notes()
    
    screen.fill((0, 0, 0))  # clears the screen

    keys = pg.key.get_pressed()
    undone = False
    round.draw_objects(screen, keys)


    resize = round.update(keys,screen,resize)

    pg.display.flip()  # updates the screen
    clock.tick(60)

pg.quit()