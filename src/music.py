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
            self.time_intervals[idx] = i + (self.get_music_delay()) #- note_offset
    
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
        intervals = intervals + notes2
        second = [24000, 24250]+[24750]+[25500]+[27500]+[28000,28250]+[28750]
        second2 = []
        for i in second:
            second2.append(i + 8000)
        intervals = intervals + second + second2
        stairs = [40750,40875]+[41000,41125,41250,41375]+[41500,41625,41750,41875]+\
            [42000,42125,42250,42375]+[42500,42625,42750,42875]+\
            [43000,43125,43250,43375]+[43500]
        stairs2 = []
        for i in stairs:
            stairs2.append(i+3875)
            stairs3 = []
        for i in stairs2:
            stairs3.append(i+3875)
            stairs4 = []
        for i in stairs3:
            stairs4.append(i+3875)
            stairs5 = []
        for i in stairs4:
            stairs5.append(i+3875)
            stairs6 = []
        for i in stairs5:
            stairs6.append(i+3875)
            stairs7 = []
        for i in stairs6:
            stairs7.append(i+3875)
        return intervals + stairs + stairs2 + stairs3 + stairs4 + stairs5 + stairs6 + stairs7
    
    def create_notes(self, key_fields):
        notes = []
        for i in self.time_intervals:
            notes.append(nt.FastNote(key_fields[i % 4]))
        #notes.insert(self.time_intervals.index(3500+8000), nt.SlowNote(key_fields[0]))
        return notes