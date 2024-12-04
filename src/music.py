import pygame as pg
import math
import notes as nt
import keyfields as kf
import playground as pgr

# these classes keep the information to build the original songs of the game
class Music:
    def __init__(self, file, speed=0, bpm=120, multiplayer=[False,1]):
        self.bpm = bpm
        # label duration: the minium time duration of a note (and minimum interval of time between notes)
        # (in miliseconds)
        self.label_duration = 60000/(4*self.bpm)
        # path of the .mp3 or .ogg
        self.file_path = file
        # interval of a note = the moment the note plays in the song (in miliseconds)
        self.time_intervals = self._create_intervals()
        # a list with all the notes (objects) that will be played
        self.notes_list = []
        self.total_notes = len(self.notes_list)
        # how fast the notes will fall
        self.speed = speed
        self.playgrounds = []
        self.multiplayer_info = multiplayer
        # a sound version of the song (needed in some cases)
        self._song = pg.mixer.Sound(file)
        self._channel = pg.mixer.Channel(1)
        self.has_panning = False
        a = pg.mixer.Sound(self.file_path)
        self.length = a.get_length()

    def _create_intervals(self):
        return
    
    def _create_notes(self, playgrounds):
        return

    def play_music(self):
        volume = 1   
        if self.has_panning: 
            self._channel.set_volume(1,0)
            volume = 0.5
        pg.mixer.music.set_volume(volume)
        pg.mixer.music.load(self.file_path)
        pg.mixer.music.play(start=0)
        
        if self.has_panning: self._channel.play(self._song)
        
    # the delay is how many miliseconds had elapsed before the song started playing
    def get_music_delay(self):
        return (pg.time.get_ticks() - pg.mixer.music.get_pos())
    
    # turns a list of integers into a list of notes, where each integer tells in which key_field the note will fall
    # slow_notes_indexes tells the index of each note that needs to be turned into a slow note. slow_notes_height tells it's size
    # fake_notes_indexes is similar to slow_notes_indexes
    def _int_to_notes(self, key_fields : list[kf.KeyField], list : list[int], slow_notes_indexes=[], fake_notes_indexes=[], slow_notes_height=[]):
        notes_list = []
        for i in list:
            notes_list.append(nt.FastNote(key_fields[i]))
        for j in slow_notes_indexes:
            kf = key_fields.index(notes_list[j].field)
            notes_list.insert(j, nt.SlowNote(key_fields[kf], height=key_fields[kf].rect.width*(1-1/6)*slow_notes_height[slow_notes_indexes.index(j)]))
            notes_list.pop(j+1)
        for k in fake_notes_indexes:
            kf = key_fields.index(notes_list[k].field)
            notes_list.insert(k, nt.FakeNote(key_fields[kf]))
            notes_list.pop(k+1)
        return notes_list
    
    def update(self):
        return
    
class ItaloMusic(Music):
    def __init__(self, file, speed=2.5, keys=[[pg.K_d,pg.K_f,pg.K_j,pg.K_k]], multiplayer=[False,1]):
        super().__init__(file, multiplayer=multiplayer)
        self.speed = speed
        
        #pg_numbers = [2,1]
        pg_numbers = [1,1]
        if multiplayer[0]:
            pg_numbers[1] = pg_numbers[0]*(multiplayer[1]-1) + 1
            pg_numbers[0] = pg_numbers[0]*2
        
        #pg_numbers2 = pg_numbers.copy()
        #pg_numbers2[1] = pg_numbers[1]+1

        self.playgrounds = [pgr.Playground(50,640,480,keys=keys[0], blank_space_percentage=0.1,pg_numbers=pg_numbers)]#,
                            #pgr.Playground(50,640,480,keys=keys[0], blank_space_percentage=0.1,pg_numbers=pg_numbers2)]
        self.notes_list = self._create_notes(self.playgrounds)
        self.total_notes = len(self.notes_list)

    def _create_intervals(self):
        intervals = [8000, 8250, 8500, 8633, 8766, 9000, 9333, 9666, 10000, 12000, 12250, 
                         12500, 12633, 12766, 13000, 13333, 13666, 14000, 16000, 16250, 16500, 
                         16633, 16766, 17000, 17333, 17666, 18000, 18250, 18500, 18633, 18766, 
                         19000, 19333, 19666, 20000, 20250, 20500, 20633, 20766, 21000, 21333, 
                         21666, 22000, 23000, 23500, 24000, 24250, 24500, 24633, 24766, 25000, 
                         25333, 25666, 26000, 26250, 26500, 26750, 26875, 27000, 27125, 27250, 
                         27375, 27500, 27750, 28000, 28250, 28500, 28750, 28875, 29250, 29375, 
                         29500, 29750, 29875, 30000, 30250, 30500, 30875, 31000, 31250, 31375, 
                         31500, 31750, 32000, 32250, 32500, 32750, 32875, 33250, 33375, 33500, 
                         33750, 34000, 34250, 34500, 34750, 34875, 35000, 35125, 35250, 35375, 
                         35500, 35750, 36000, 36250, 36500, 36750, 36875, 37250, 37375, 37500, 
                         37750, 37875, 38000, 38250, 38500, 38875, 39000, 39250, 39375, 39500, 
                         39750, 40000, 40250, 40500, 40750, 40875, 41250, 41375, 41500, 41750, 
                         42000, 42250, 42500, 42750, 42875, 43000, 43125, 43250, 43375, 43500, 
                         43750, 44000, 44250, 44500, 44750, 44875, 45250, 45375, 45500, 45750, 
                         45875, 46000, 46250, 46500, 46875, 47000, 47250, 47375, 47500, 47750, 
                         48000, 48250, 48500, 48750, 48875, 49250, 49375, 49500, 49750, 50000, 
                         50250, 50500, 50750, 50875, 51000, 51125, 51250, 51375, 51500, 51750, 
                         52000, 52250, 52500, 52750, 52875, 53250, 53375, 53500, 53750, 53875, 
                         54000, 54250, 54500, 54875, 55000, 55250, 55375, 55500, 55750, 56000, 
                         56250, 56500, 56750, 56875, 57250, 57375, 57500, 57750]
        return intervals

    def _create_notes(self, playgrounds):
        ints_list = [0, 0, 1, 2, 1, 3, 3, 2, 0, 0, 0, 1, 2, 1, 3, 3, 3, 2, 0, 0, 1, 2, 1, 3, 3, 3, 0, 0, 1, 2, 1, 3, 3, 3, 
                     2, 2, 1, 2, 1, 0, 0, 0, 1, 2, 3, 0, 0, 1, 2, 1, 2, 2, 2, 0, 0, 0, 1, 0, 2, 1, 2, 1, 0, 1, 3, 2, 2, 3, 
                     2, 2, 3, 2, 0, 1, 0, 0, 3, 1, 2, 3, 2, 1, 1, 2, 2, 2, 1, 2, 1, 0, 1, 0, 0, 0, 0, 1, 0, 2, 1, 2, 1, 0, 
                     1, 3, 2, 2, 3, 2, 2, 3, 2, 0, 1, 0, 0, 3, 1, 2, 3, 2, 1, 1, 2, 2, 2, 1, 2, 1, 0, 1, 0, 0, 0, 0, 1, 0, 
                     2, 1, 2, 1, 0, 1, 3, 2, 2, 3, 2, 2, 3, 2, 0, 1, 0, 0, 3, 1, 2, 3, 2, 1, 1, 2, 2, 2, 1, 2, 1, 0, 1, 0, 
                     0, 0, 0, 1, 0, 2, 1, 2, 1, 0, 1, 3, 2, 2, 3, 2, 2, 3, 2, 0, 1, 0, 0, 3, 1, 2, 3, 2, 1, 1, 2, 2, 2, 1, 
                     2, 1, 0, 1, 0]
        slow_notes = [8, 17, 42, 43, 44]
        slow_heights = [24, 24, 12, 5, 5]
        return self._int_to_notes(playgrounds[0].key_fields, ints_list, slow_notes, slow_notes_height=slow_heights)


class StardewMusic(Music):

    def __init__(self, file, speed=2, keys=[[pg.K_d,pg.K_f,pg.K_j,pg.K_k]], multiplayer=[False,1]):
        super().__init__(file, multiplayer=multiplayer)
        
        pg_numbers = [1,1]
        if multiplayer[0]:
            pg_numbers[1] = pg_numbers[0]*(multiplayer[1]-1) + 1
            pg_numbers[0] = pg_numbers[0]*2
        
        self.playgrounds = [pgr.Playground(50,640,480,keys=keys[0], blank_space_percentage=0.1,pg_numbers=pg_numbers)]
        self.speed = speed
        self.notes_list = self._create_notes(self.playgrounds)
        self.total_notes = len(self.notes_list)

    def _create_intervals(self):
        intervals = [8000, 8250, 8625, 8875, 9000, 9125, 9250, 9500, 9750, 10000, 10250, 10500, 
                     10750, 10875, 11000, 11125, 11375, 11500, 11750, 12000, 12250, 12625, 12875, 
                     13000, 13125, 13250, 13500, 13750, 14000, 14250, 14500, 14750, 14875, 15125, 
                     15125, 15375, 15375, 15500, 15500, 16000, 16250, 16625, 16875, 17000, 17125, 
                     17250, 17500, 17750, 18000, 18250, 18500, 18750, 18875, 19000, 19125, 19375, 
                     19500, 19750, 20000, 20250, 20625, 20875, 21000, 21125, 21250, 21500, 21750, 
                     22000, 22250, 22500, 22750, 22875, 23125, 23125, 23375, 23375, 23500, 23500, 
                     24000, 24250, 24750, 25500, 27500, 28000, 28250, 28750, 32000, 32250, 32750, 
                     33500, 35500, 36000, 36250, 36750, 40000, 40125, 40250, 40375, 40500, 40625, 
                     40750, 40875, 41000, 41125, 41250, 41375, 41500, 41625, 41750, 41875, 42000, 
                     42125, 42250, 42375, 42500, 42625, 42750, 42875, 43000, 43125, 43250, 43375, 
                     43500, 44000, 44125, 44250, 44375, 44500, 44625, 44750, 44875, 45000, 45125, 
                     45250, 45375, 45500, 45625, 45750, 45875, 46000, 46125, 46250, 46375, 46500, 
                     46625, 46750, 46875, 47000, 47125, 47250, 47375, 47500, 48000, 48125, 48250, 
                     48375, 48500, 48625, 48750, 48875, 49000, 49125, 49250, 49375, 49500, 49625, 
                     49750, 49875, 50000, 50125, 50250, 50375, 50500, 50625, 50750, 50875, 51000, 
                     51125, 51250, 51375, 51500, 52000, 52125, 52250, 52375, 52500, 52625, 52750, 
                     52875, 53000, 53125, 53250, 53375, 53500, 53625, 53750, 53875, 54000, 54125, 
                     54250, 54375, 54500, 54625, 54750, 54875, 55000, 55125, 55250, 55375, 55500, 
                     56000, 56250, 56625, 56875, 57000, 57125, 57250, 57500, 57750, 58000, 58250, 
                     58500, 58750, 58875, 59000, 59125, 59375, 59500, 59750, 60000, 60250, 60625, 
                     60875, 61000, 61125, 61250, 61500, 61750, 62000, 62250, 62500, 62750, 62875, 
                     63125, 63125, 63375, 63375, 63500, 63500, 64000, 64250, 64625, 64875, 65000, 
                     65125, 65250, 65500, 65750, 66000, 66250, 66500, 66750, 66875, 67000, 67125, 
                     67375, 67500, 67750, 68000, 68250, 68625, 68875, 69000, 69125, 69250, 69500, 
                     69750, 70000, 70250, 70500, 70750, 70875, 71125, 71125, 71375, 71375, 71500, 
                     71500, 72000, 72750, 73750, 74000, 74750, 75750, 76000, 76750, 77750, 78000, 
                     78750, 79500, 80000, 80750, 81750, 82000, 82750, 83750, 84000, 84750, 85750, 
                     86000, 86750, 87500, 88000, 88250, 88500, 88625, 88750, 88875, 89125, 89250, 
                     89375, 89500, 90000, 90250, 90500, 90750, 90875, 91000, 91125, 91250, 91375, 
                     91500, 91625, 91750, 91875, 92000, 92125, 92250, 92375, 92500, 92675, 92750, 
                     92875, 93000, 93125, 93250, 94000, 94250, 94750, 96000, 96000, 96250, 96625, 
                     96875, 97000, 97125, 97250, 97500, 97750, 98000, 98000, 98250, 98500, 98750, 
                     98875, 99000, 99125, 99375, 99500, 99750, 100000, 100000, 100250, 100625, 
                     100875, 101000, 101125, 101250, 101500, 101750, 102000, 102000, 102250, 
                     102500, 102750, 102875, 104000, 104000, 104250, 104625, 104875, 105000, 
                     105125, 105250, 105500, 105750, 106000, 106000, 106250, 106500, 106750, 
                     106875, 107000, 107125, 107375, 107500, 107750, 108000, 108000, 108250, 
                     108625, 108875, 109000, 109125, 109250, 109500, 109750, 110000, 110000, 
                     110250, 110500, 110750, 110875]
        return intervals
    
    def _create_notes(self, playgrounds : list[pgr.Playground]):
        notes = []
        last = 0
        inc = 0
        for i in self.time_intervals:
            if ((i > 15000 and i < 15625) or (i > 23000 and i < 23501)):
                notes.append(nt.FastNote(playgrounds[0].key_fields[1+inc]))
                inc = (inc + 1) % 2
            elif ((i > 63000 and i < 63501) or (i > 71000 and i < 71501)):
                notes.append(nt.FastNote(playgrounds[0].key_fields[3*inc]))
                inc = (inc + 1) % 2
            elif last != i and i < 95000:
                notes.append(nt.FastNote(playgrounds[0].key_fields[i % 4]))
            elif last != i and i % 2000 == 0:
                notes.append(nt.FastNote(playgrounds[0].key_fields[i % 3]))
                notes.append(nt.FastNote(playgrounds[0].key_fields[(i % 3) + 1]))
                last = i
            elif last != i:
                notes.append(nt.FastNote(playgrounds[0].key_fields[i % 4]))
                
            last = i
        return notes
    
class StakesMusic(Music):
    def __init__(self, file, speed=2, keys=[[pg.K_d,pg.K_f,pg.K_j,pg.K_k]], multiplayer=[False,1]):
        super().__init__(file, speed, 111, multiplayer)
        self.has_panning = True
        
        pg_numbers = [2,1]
        
        if multiplayer[0]:
            pg_numbers[1] = pg_numbers[0]*(multiplayer[1]-1) + 1
            pg_numbers[0] = pg_numbers[0]*2
            
        pg_numbers2 = pg_numbers.copy()
        pg_numbers2[1] = pg_numbers[1] + 1
        
        self.playgrounds = [pgr.Playground(50,640,480,keys=keys[0], blank_space_percentage=0.1,pg_numbers=pg_numbers),
                            pgr.Playground(50,640,480,keys=keys[0], blank_space_percentage=0.1,pg_numbers=pg_numbers2)]
        self.speed = speed
        self.notes_list = self._create_notes(self.playgrounds)
        self.total_notes = len(self.notes_list)
        
        
    def _create_intervals(self):        
        intervals = [
             (
              [8649, 8919, 9189, 9324, 9595, 10811, 11081, 11351, 11486, 11757, 12973, 13243, 13514, 13649, 13919, 15135, 15405, 15676, 15811, 
               16081, 31622, 31757, 32027, 32162, 32568, 33514, 33784, 34054, 34189, 34595, 35946, 36081, 36351, 36486, 36757, 37838, 38108, 
               38378, 38514, 38919, 40000, 40270, 40405, 40676, 40811, 41081, 42162, 43243, 44459, 44595, 45000, 45135, 45270, 46486, 47568, 
               48649, 49730, 50811, 69189, 70135, 70541, 71081, 71351, 72432, 72973, 77838, 77973, 78108, 78243, 78649, 78784, 78919, 79054, 
               80000, 81216, 95135, 95405, 95676, 95811, 96081, 97297, 97568, 97838, 97973, 98243, 103919, 104054, 104324, 104459, 104730], 
              [17297, 17568, 17838, 17973, 18243, 19459, 19730, 20000, 20135, 20405, 21622, 21892, 22162, 22297, 22568, 23784, 24054, 24324, 
               24459, 24730, 25946, 26216, 26486, 26622, 26892, 28108, 28378, 28649, 28784, 29054, 29324, 29459, 29595, 30000, 30270, 51892, 
               53243, 53378, 53649, 53784, 54189, 55135, 55405, 55676, 55811, 56216, 57297, 57568, 57703, 57973, 58108, 58514, 59459, 60541, 
               61757, 62027, 62297, 62432, 62568, 63784, 64865, 65946, 67027, 68108, 73514, 74459, 74865, 75405, 75676, 76757, 77297, 82162, 
               82297, 82432, 82568, 82973, 83108, 83243, 83378, 83514, 84054, 84189, 84324, 84459, 84595, 85541, 85946, 86486, 99595, 99730, 
               100000, 100135, 100405, 101757, 101892, 102162, 102297, 102568]
             ), 
             [8649, 8919, 9189, 9324, 9595, 10811, 11081, 11351, 11486, 11757, 12973, 13243, 13514, 13649, 13919, 15135, 15405, 15676, 15811, 
              16081, 17297, 17568, 17838, 17973, 18243, 19459, 19730, 20000, 20135, 20405, 21622, 21892, 22162, 22297, 22568, 23784, 24054, 24324, 
              24459, 24730, 25946, 26216, 26486, 26622, 26892, 28108, 28378, 28649, 28784, 29054, 29324, 29459, 29595, 30000, 30270, 31622, 31757, 
              32027, 32162, 32568, 33514, 33784, 34054, 34189, 34595, 35946, 36081, 36351, 36486, 36757, 37838, 38108, 38378, 38514, 38919, 40000, 
              40270, 40405, 40676, 40811, 41081, 42162, 43243, 44459, 44595, 45000, 45135, 45270, 46486, 47568, 48649, 49730, 50811, 51892, 53243, 
              53378, 53649, 53784, 54189, 55135, 55405, 55676, 55811, 56216, 57297, 57568, 57703, 57973, 58108, 58514, 59459, 60541, 61757, 62027, 
              62297, 62432, 62568, 63784, 64865, 65946, 67027, 68108, 69189, 70135, 70541, 71081, 71351, 72432, 72973, 73514, 74459, 74865, 75405, 
              75676, 76757, 77297, 77838, 77973, 78108, 78243, 78649, 78784, 78919, 79054, 80000, 81216, 82162, 82297, 82432, 82568, 82973, 83108, 
              83243, 83378, 83514, 84054, 84189, 84324, 84459, 84595, 85541, 85946, 86486, 95135, 95405, 95676, 95811, 96081, 97297, 97568, 97838, 
              97973, 98243, 99595, 99730, 100000, 100135, 100405, 101757, 101892, 102162, 102297, 102568, 103919, 104054, 104324, 104459, 104730]
            ]
        
        return intervals
    
    
    def _create_notes(self,playgrounds : list[pgr.Playground]):
        notes = []
        
        columns = [0, 0, 1, 0, 1, 2, 2, 3, 2, 3, 0, 0, 1, 0, 1, 2, 2, 3, 2, 3, 0, 0, 3, 0, 3, 1, 1, 2, 1, 2, 0, 0, 
        3, 0, 3, 1, 1, 2, 1, 2, 0, 0, 3, 0, 3, 1, 1, 2, 1, 2, 0, 1, 2, 1, 3, 0, 1, 2, 3, 2, 1, 0, 1, 0, 0, 1, 2, 3, 
        2, 3, 0, 1, 2, 3, 2, 1, 3, 1, 3, 1, 2, 3, 0, 1, 0, 1, 0, 1, 2, 3, 3, 2, 1, 0, 0, 1, 1, 2, 3, 2, 3, 2, 3, 2, 0, 
        1, 2, 3, 2, 3, 0, 1, 2, 3, 1, 2, 1, 3, 3, 2, 1, 0, 1, 1, 1, 1, 2, 3, 0, 3, 1, 1, 1, 2, 0, 3, 0, 2, 1, 3, 1, 
        2, 1, 2, 0, 1, 2, 3, 2, 3, 0, 2, 1, 2, 1, 0, 2, 1, 2, 1, 3, 0, 2, 0, 1, 0, 1, 0, 2, 3, 2, 3, 2, 1, 2, 1, 
        2, 1, 0, 3, 0, 3, 0, 1, 2, 1, 2, 1]

        for i in self.time_intervals[1]:
            if self.time_intervals[0][0].count(i) != 0:
                notes.append(nt.FastNote(playgrounds[0].key_fields[columns[self.time_intervals[1].index(i)]]))
            elif self.time_intervals[0][1].count(i) != 0:
                notes.append(nt.FastNote(playgrounds[1].key_fields[columns[self.time_intervals[1].index(i)]]))
        
        self.time_intervals = self.time_intervals[1]
        
        return notes
    
    
    def update(self):
        music_pos = pg.mixer.music.get_pos()        
        right_triggers = [0, 30270, 68108, 77297, 86486, 102568]
        left_triggers = [0, 16081, 50811, 72973, 81216, 98243, 104730]
        
        for i in range(len(left_triggers)-1):
            if left_triggers[i] <= music_pos and right_triggers[i] >= music_pos:
                self._channel.set_volume(0,1)
        for i in range(len(right_triggers)):
            if right_triggers[i] <= music_pos and left_triggers[i+1] >= music_pos:
                self._channel.set_volume(1,0)