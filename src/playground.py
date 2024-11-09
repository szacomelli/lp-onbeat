import pygame as pg
import notes as nt, keyfields as kf, currentround as cr

class Playground:
    def __init__(self, x, bottom_padding, length, screen_height, keys=[pg.K_s, pg.K_d, pg.K_k, pg.K_l],blank_space_percentage=0.1):
        self.info = [length,screen_height,x,bottom_padding]
        self.blank_space = blank_space_percentage*length
        self.key_field_size = (length - self.blank_space*3)/4
        self.interval = self.key_field_size+self.blank_space
        self.bottom_padding = bottom_padding
        kf_x = [x,x+self.interval,x+self.interval*2,x+self.interval*3]
        kf_y = screen_height - bottom_padding
        self.keys = keys
        self.key_fields = [kf.KeyField(kf_x[0], kf_y, (255, 0, 0), (220, 0, 0), keys[0], size=self.key_field_size),
              kf.KeyField(kf_x[1], kf_y, (0, 255, 0), (0, 220, 0), keys[1],size=self.key_field_size), 
              kf.KeyField(kf_x[2], kf_y, (0, 0, 255), (0, 0, 220), keys[2],size=self.key_field_size), 
              kf.KeyField(kf_x[3], kf_y, (255, 255, 0), (220, 220, 0), keys[3],size=self.key_field_size),]
        self.first_update = True
    

    def update(self,screen,update_ratios,speed,screen_size=[480,640]):
        width_ratio = screen.get_width() / screen_size[1]
        height_ratio = screen.get_height() / screen_size[0]
        
        self.bottom_padding = self.bottom_padding*height_ratio
        self.interval = self.interval * width_ratio
        self.key_field_size = self.key_field_size * width_ratio
        bias = self.key_field_size*(1/6)

        x = self.info[2]*width_ratio
        y = screen.get_height() - self.bottom_padding - self.key_field_size
        for i in self.key_fields:
            i.bias = bias
            i.rect.x = x
            i.rect.y = y
            x = x + self.interval
            
            i.rect.width = self.key_field_size
            i.rect.height = self.key_field_size

        if width_ratio != 1:
            speed = speed / width_ratio
        
        update_ratios(max(width_ratio,height_ratio))
        self.info[2] = self.info[2]*width_ratio

        return ([screen.get_height(),screen.get_width()], speed)
        