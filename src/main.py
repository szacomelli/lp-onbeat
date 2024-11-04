import pygame as pg
from threading import Timer as tm
import notes as nt, keyfields as kf, actualround as ar 

pg.mixer.pre_init(44100, channels=2, buffer=512)
pg.mixer.init()
pg.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def trines(i):
    return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i+1]), nt.FastNote(key_fields[i])]
def threes(i):
    return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i])]
def doubles(i):
    return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i])]
def broken(i):
    return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i+1]), nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i+1]), nt.FastNote(key_fields[i+1])]
def two(i):
    return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i-1])]
def two_inv(i):
    return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i+1])]
def two_one(i):
    return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i+1]), nt.FastNote(key_fields[i+1])]


clock = pg.time.Clock()
a = [0, 2, 7, 13]
key_fields = [kf.KeyField(100, 400, (255, 0, 0), (220, 0, 0), pg.K_s, a),
              kf.KeyField(200, 400, (0, 255, 0), (0, 220, 0), pg.K_d, a), 
              kf.KeyField(300, 400, (0, 0, 255), (0, 0, 220), pg.K_k, a), 
              kf.KeyField(400, 400, (255, 255, 0), (220, 220, 0), pg.K_l, a)]

notes_list = [nt.FastNote(key_fields[0]), nt.FastNote(key_fields[0]), nt.FastNote(key_fields[1]), nt.FastNote(key_fields[2]), nt.FastNote(key_fields[1]), 
              nt.FastNote(key_fields[3]), nt.FastNote(key_fields[3]), nt.FastNote(key_fields[2]), nt.SlowNote(key_fields[0], height=200),

              nt.FastNote(key_fields[0]), nt.FastNote(key_fields[0]), nt.FastNote(key_fields[1]), nt.FastNote(key_fields[2]), nt.FastNote(key_fields[1]), 
              nt.FastNote(key_fields[3]), nt.FastNote(key_fields[3]), nt.FastNote(key_fields[3]), nt.SlowNote(key_fields[2], height=200),
              
              nt.FastNote(key_fields[0]), nt.FastNote(key_fields[0]), nt.FastNote(key_fields[1]), nt.FastNote(key_fields[2]), nt.FastNote(key_fields[1]), 
              nt.FastNote(key_fields[3]), nt.FastNote(key_fields[3]), nt.FastNote(key_fields[3]), nt.FastNote(key_fields[0]),
              nt.FastNote(key_fields[0]), nt.FastNote(key_fields[1]), nt.FastNote(key_fields[2]), nt.FastNote(key_fields[1]), nt.FastNote(key_fields[3]), 
              nt.FastNote(key_fields[3]), nt.FastNote(key_fields[3]), nt.FastNote(key_fields[2]), nt.FastNote(key_fields[2]), nt.FastNote(key_fields[1]),
              nt.FastNote(key_fields[2]), nt.FastNote(key_fields[1]), nt.FastNote(key_fields[0]), nt.FastNote(key_fields[0]), nt.FastNote(key_fields[0]), 
              nt.SlowNote(key_fields[1], height=200), nt.SlowNote(key_fields[2], height=100), nt.SlowNote(key_fields[3], height=100)
              ] + doubles(0) + trines(1) + threes(2)

notes_refrao = doubles(0) + trines(0) + two(2) + two(2) + two_inv(0) + two(3) + trines(2) + trines(2) + trines(0) + [nt.FastNote(key_fields[0]), nt.FastNote(key_fields[3])] \
+[nt.FastNote(key_fields[1])] + trines(2) + doubles(1) + threes(2) + trines(1) + two_inv(0) +  [nt.FastNote(key_fields[0])] \
+doubles(0) + trines(0) + two(2) + two(2) + two_inv(0) + two(3) + trines(2) + trines(2) + trines(0) + [nt.FastNote(key_fields[0]), nt.FastNote(key_fields[3])] \
+[nt.FastNote(key_fields[1])] + trines(2) + doubles(1) + threes(2) + trines(1) + two_inv(0) + [nt.FastNote(key_fields[0])] + \
doubles(0) + trines(0) + two(2) + two(2) + two_inv(0) + two(3) + trines(2) + trines(2) + trines(0) + [nt.FastNote(key_fields[0]), nt.FastNote(key_fields[3])] \
+[nt.FastNote(key_fields[1])] + trines(2) + doubles(1) + threes(2) + trines(1) + two_inv(0)+ [nt.FastNote(key_fields[0])] +\
doubles(0) + trines(0) + two(2) + two(2) + two_inv(0) + two(3) + trines(2) + trines(2) + trines(0) + [nt.FastNote(key_fields[0]), nt.FastNote(key_fields[3])] \
+[nt.FastNote(key_fields[1])] + trines(2) + doubles(1) + threes(2) + trines(1) + two_inv(0) + [nt.FastNote(key_fields[0])]

print(len(notes_list))
notes_list = notes_list + notes_refrao.copy() #+ notes_refrao.copy() + notes_refrao.copy() + notes_refrao.copy()
print(len(notes_refrao), len(notes_list))
intervals = [8000, 8250] + [8500, 8633, 8766, 9000, 9333, 9666, 10000, 12000, 12250, 12500, 12633, 12766, 13000, 13333, 13666, 14000,
16000, 16250, 16500, 16633, 16766, 17000, 17333, 17666, 18000, 18250, 18500, 18633, 18766, 19000, 19333, 19666, 20000, 20250, 20500, 20633, 20766,
21000, 21333, 21666, 22000, 23000, 23500] + [24000, 24250] + [24500, 24633, 24766]+ [25000, 25333, 25666]
refrao = [26000, 26250] + [26500, 26750, 26875] + [27000, 27125, 27250, 27375] + [27500, 27750] + [28000, 28250] + [28500, 28750, 28875, 29250, 29375] + [29500, 29750, 29875] + [30000, 30250] + [30500,
 30875, 31000, 31250, 31375] + [31500, 31750] + [32000, 32250] + [32500, 32750, 32875, 33250, 33375] + [33500, 33750]
refrao_2 = [i+8000 for i in refrao]
refrao_3 = [i+8000 for i in refrao_2]
refrao_4 = [i+8000 for i in refrao_3]

intervals = intervals + refrao + refrao_2 + refrao_3 + refrao_4

pg.mixer.music.load("./FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3")
pg.mixer.music.play()

print(intervals)
print(len(intervals), len(notes_list))
for i in intervals:
    idx = intervals.index(i)
    intervals[idx] = i + (pg.time.get_ticks() - pg.mixer.music.get_pos()) - 2700

print(intervals)

#

print(pg.mixer.get_init())

round = ar.ActualRound(key_fields, notes_list, intervals)
running = True
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
    clock.tick(30)

pg.quit()