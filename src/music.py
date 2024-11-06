import pygame as pg
import math
import notes as nt
import keyfields as kf

class Music:
    def __init__(self, file, key_fields):
        self.file_path = file
        self.time_intervals = self.create_intervals()
        self.notes_list = self.create_notes(key_fields)
        self.total_notes = len(self.notes_list)

    def create_intervals(self):
        return
    
    def create_notes(self, key_fields):
        return

    def play_music(self):
        pg.mixer.music.load("./FullScores/Retro Scores/Ove Melaa - Italo Unlimited.mp3")
        pg.mixer.music.play()

    def get_music_delay(self):
        return (pg.time.get_ticks() - pg.mixer.music.get_pos())
    
    def update_intervals(self, note_offset=1200):
        for i in self.time_intervals:
            idx = self.time_intervals.index(i)
            self.time_intervals[idx] = i# + (self.get_music_delay()) #- note_offset
    
class ItaloMusic(Music):
    def __init__(self, file, key_fields : kf.KeyField):
        super().__init__(file, key_fields)

    def create_intervals(self):
        intervals = [8000, 8250] + [8500, 8633, 8766, 9000, 9333, 9666, 10000, 12000, 12250, 12500, 12633, 12766, 13000, 13333, 13666, 14000,
        16000, 16250, 16500, 16633, 16766, 17000, 17333, 17666, 18000, 18250, 18500, 18633, 18766, 19000, 19333, 19666, 20000, 20250, 20500, 20633, 20766,
        21000, 21333, 21666, 22000, 23000, 23500] + [24000, 24250] + [24500, 24633, 24766]+ [25000, 25333, 25666]
        refrao = [26000, 26250] + [26500, 26750, 26875] + [27000, 27125, 27250, 27375] + [27500, 27750] + [28000, 28250] + [28500, 28750, 28875, 29250, 29375] + [29500, 29750, 29875] + [30000, 30250] + [30500,
        30875, 31000, 31250, 31375] + [31500, 31750] + [32000, 32250] + [32500, 32750, 32875, 33250, 33375] + [33500, 33750]
        refrao_2 = [i+8000 for i in refrao]
        refrao_3 = [i+8000 for i in refrao_2]
        refrao_4 = [i+8000 for i in refrao_3]

        return intervals + refrao + refrao_2 + refrao_3 + refrao_4

    def create_notes(self, key_fields):
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
              ] + self.doubles(0, key_fields) + self.trines(1, key_fields) + self.threes(2, key_fields)

        notes_refrao = self.doubles(0, key_fields) + self.trines(0, key_fields) + self.two(2, key_fields) + self.two(2, key_fields) + self.two_inv(0, key_fields) + self.two(3, key_fields) + self.trines(2, key_fields) + self.trines(2, key_fields) + self.trines(0, key_fields) + [nt.FastNote(key_fields[0]), nt.FastNote(key_fields[3])] \
        +[nt.FastNote(key_fields[1])] + self.trines(2, key_fields) + self.doubles(1, key_fields) + self.threes(2, key_fields) + self.trines(1, key_fields) + self.two_inv(0, key_fields) +  [nt.FastNote(key_fields[0])] \
        +self.doubles(0, key_fields) + self.trines(0, key_fields) + self.two(2, key_fields) + self.two(2, key_fields) + self.two_inv(0, key_fields) + self.two(3, key_fields) + self.trines(2, key_fields) + self.trines(2, key_fields) + self.trines(0, key_fields) + [nt.FastNote(key_fields[0]), nt.FastNote(key_fields[3])] \
        +[nt.FastNote(key_fields[1])] + self.trines(2, key_fields) + self.doubles(1, key_fields) + self.threes(2, key_fields) + self.trines(1, key_fields) + self.two_inv(0, key_fields) + [nt.FastNote(key_fields[0])] + \
        self.doubles(0, key_fields) + self.trines(0, key_fields) + self.two(2, key_fields) + self.two(2, key_fields) + self.two_inv(0, key_fields) + self.two(3, key_fields) + self.trines(2, key_fields) + self.trines(2, key_fields) + self.trines(0, key_fields) + [nt.FastNote(key_fields[0]), nt.FastNote(key_fields[3])] \
        +[nt.FastNote(key_fields[1])] + self.trines(2, key_fields) + self.doubles(1, key_fields) + self.threes(2, key_fields) + self.trines(1, key_fields) + self.two_inv(0, key_fields)+ [nt.FastNote(key_fields[0])] +\
        self.doubles(0, key_fields) + self.trines(0, key_fields) + self.two(2, key_fields) + self.two(2, key_fields) + self.two_inv(0, key_fields) + self.two(3, key_fields) + self.trines(2, key_fields) + self.trines(2, key_fields) + self.trines(0, key_fields) + [nt.FastNote(key_fields[0]), nt.FastNote(key_fields[3])] \
        +[nt.FastNote(key_fields[1])] + self.trines(2, key_fields) + self.doubles(1, key_fields) + self.threes(2, key_fields) + self.trines(1, key_fields) + self.two_inv(0, key_fields) + [nt.FastNote(key_fields[0])]


        return notes_list + notes_refrao.copy()        

    def trines(self, i, key_fields):
        return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i+1]), nt.FastNote(key_fields[i])]
    def threes(self, i, key_fields):
        return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i])]
    def doubles(self, i, key_fields):
        return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i])]
    def broken(self, i, key_fields):
        return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i+1]), nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i+1]), nt.FastNote(key_fields[i+1])]
    def two(self, i, key_fields):
        return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i-1])]
    def two_inv(self, i, key_fields):
        return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i+1])]
    def two_one(self, i, key_fields):
        return [nt.FastNote(key_fields[i]), nt.FastNote(key_fields[i+1]), nt.FastNote(key_fields[i+1])]



class StardewMusic(Music):

    def __init__(self, file, key_fields : kf.KeyField):
        super().__init__(file, key_fields)

    def create_intervals(self):
        intervals = [0, 250]+[625,875]+[1000,1125,1250]+[1500,1750]+[2000,2250]+\
        [2500,2750,2875]+[3000,3125,3375]+[3500,3750]+[4000,4250]+[4625,4875]+\
        [5000,5125,5250]+[5500,5750]+[6000,6250]+[6500,6750,6875]

        for i in intervals:
            intervals[intervals.index(i)] += 8000
        notes2 = []
        for i in intervals:
            notes2.append(i+8000)
        second = [24000, 24250]+[24750]+[25500]+[27500]+[28000,28250]+[28750]
        second2 = []
        for i in second:
            second2.append(i + 8000)

        stairs = [40000, 40125, 40250, 40375] + [40500, 40625, 40750,40875]+[41000,41125,41250,41375]+[41500,41625,41750,41875]+\
            [42000,42125,42250,42375]+[42500,42625,42750,42875]+\
            [43000,43125,43250,43375]+[43500]
        
        stairs2 = []
        for i in stairs:
            stairs2.append(i+4000)
            stairs3 = []
        for i in stairs2:
            stairs3.append(i+4000)
            stairs4 = []
        for i in stairs3:
            stairs4.append(i+4000)
        notes3 = []
        for i in notes2:
            notes3.append(i + 40000)
        notes4 = []
        for i in notes3:
            notes4.append(i + 8000)

        joyful = [72000, 72750]+[73750]+[74000,74750]+[75750]+\
                [76000,76750]+[77750]+[78000,78750]+[79500]
        
        joyful2 = []
        for i in joyful:
            joyful2.append(i+8000)

        lasts=[88000,88250,88500,88625,88750,88875]+[89125,89250,89375,89500]+\
            [90000,90250,90500,90750,90875]+[91000,91125,91250,91375,91500]+\
            [91625,91750,91875]+[92000,92125,92250,92375]+[92500,92675,92750,92875]+\
            [93000,93125,93250]+[94000,94250,94750]
        
        lasts2 = []
        for i in notes4:
            lasts2.append(i+32000)
            if (i+32000) % 2000 == 0:
                lasts2.append(i+32000)
            
        lasts3 = []
        for i in lasts2:
            lasts3.append(i+8000)
            
        new_intervals=intervals + notes2 + second + second2 + stairs + stairs2 + stairs3 + stairs4 + notes3 + notes4 + joyful + joyful2 + lasts + lasts2 + lasts3
        # print(notes4)
        return new_intervals
    
    def create_notes(self, key_fields):
        notes = []
        last = 0
        for i in self.time_intervals:
            if i < 95000:
                notes.append(nt.FastNote(key_fields[i % 4]))
            elif last != i and i % 2000 == 0:
                notes.append(nt.FastNote(key_fields[i % 3]))
                notes.append(nt.FastNote(key_fields[(i % 3) + 1]))
                last = i
            else:
                notes.append(nt.FastNote(key_fields[i % 4]))
                last = i
        #notes.insert(self.time_intervals.index(3500+8000), nt.SlowNote(key_fields[0]))
        return notes