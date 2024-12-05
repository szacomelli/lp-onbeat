import pygame as pg
import currentround as cr, music as ms, playground as pgr
import devmode as dv

pg.mixer.pre_init(44100, channels=2, buffer=512)
pg.mixer.init()
pg.init()


screen_size = [480,640]
screen = pg.display.set_mode((screen_size[1], screen_size[0]), pg.RESIZABLE)

clock = pg.time.Clock()

#dev_i = int(input("Enter creation mode (to create your music, edit src/config/music_test.json)?\n 1. Yes\n 2. No\nInput your answer: "))
dev = True #if dev_i == 1 else False

if dev: music_name = input("Input the name of the music\n (if you input an invalid name a new music will be created)\
    \n (input e to edit a music): ") 
else: music_name = "Musica2"

if music_name == "e": 
    editing_music = True 
    music_name = input("Name the music to edit: ")
else: editing_music = False


devmode = dv.DevMode(music_name, active=dev, editing_music=editing_music)

if not dev: 
    music = int(input("Select a music:\n 0. Italo\n 1. Tropicala\n 2. Stakes\nInput your answer: "))


if not dev: players = int(input("Number of players (1 or 2): "))
else: players = 1
mult = [True, 1]
if players == 1:
    mult[0] = False

musicas = []
rounds = []
resizes = []

if players == 1:
    keys=[[[pg.K_d,pg.K_f,pg.K_j,pg.K_k], pg.K_SPACE]]
elif players == 2:
    keys=[[[pg.K_q,pg.K_w,pg.K_e,pg.K_r], pg.K_z],[[pg.K_o,pg.K_p,pg.K_LEFTBRACKET,pg.K_RIGHTBRACKET],pg.K_PERIOD]]

# for i in range(players):
#     if mult[0]: mult[1] = mult[1] + i
#     if dev: 
#         musicas.append(3)
#     else:
#         if music == 0: musicas.append(ms.ItaloMusic("./FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3", keys=keys[i], multiplayer=mult))
#         elif music == 1: musicas.append(ms.StardewMusic("./Tropicalia-short.mp3", keys=keys[i], multiplayer=mult))
#         else: musicas.append(ms.StakesMusic("./FullScores/Retro Scores/Ove Melaa - High Stakes,Low Chances.mp3", keys=keys[i], multiplayer=mult))
#     rounds.append(cr.CurrentRound(music=musicas[i], switch_key=keys[i][1], dev=dev, music_name=music_name, editing_music=editing_music))
#     resizes.append(False)

# rounds = [cr.CurrentRound(music=3, switch_key=keys[0][1], dev=dev)]
# resizes = [False]

#rounds[0].start_round()
devmode.round.start_round()
running = True
resize = False
resize2=False

while running:
    for event in pg.event.get():
        # for round in rounds:
        #     round.on_event(event)
        devmode.on_event(event)
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.VIDEORESIZE:
            # for i in range(players):
            #     resizes[i] = True
            resize = True
        
    # for round in rounds:
    #     round.play_notes()
    devmode.round.play_notes()
    
    screen.fill((0, 0, 0))  # clears the screen

    keys_pressed = pg.key.get_pressed()
    undone = False
    
    devmode.round.draw_objects(screen, keys_pressed)
    devmode.draw_selection(screen, devmode.round.notes_to_play, devmode.round.music_start_pos, devmode.round.stop_index)
    devmode.draw(screen, devmode.round.music_start_pos, devmode.round.text_font)
    # for round in rounds:
    #     round.draw_objects(screen, keys_pressed)
    #     if dev: dev.draw_selection(screen, round.notes_to_play, round.music_start_pos, round.stop_index, round.round_callback)
    #     if dev: dev.draw(screen, round.music_start_pos, round.text_font)

    # for i in range(players):
    #     resizes[i] = rounds[i].update(keys_pressed,screen,resizes[i], dev=rounds[i].dev)
    resize = devmode.round.update(keys_pressed,screen,resize, dev=devmode)

    pg.display.flip()  # updates the screen
    clock.tick(60)

pg.quit()