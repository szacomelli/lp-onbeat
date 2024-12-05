import pygame as pg
import notes as nt, keyfields as kf

<<<<<<< HEAD

=======
# playground takes the "box" that contains the key_fields and notes and resizes it as the screen resizes too
>>>>>>> main
class Playground:
    def __init__(self, bottom_padding, screen_width, screen_height, black_bars=50, keys=[pg.K_s, pg.K_d, pg.K_k, pg.K_l], blank_space_percentage=0.1, pg_numbers=[1,1]):
        usable_width = screen_width-2*black_bars
        
        playground_width = (usable_width)/pg_numbers[0]
        start= (pg_numbers[1]-1)*(usable_width)/pg_numbers[0] + black_bars 
        
        
        lateral_padding = playground_width*0.1 
        length = min(playground_width - 2*lateral_padding, 175)
        x = max(lateral_padding, (playground_width - length)/2)
        x = x + start
        
        self.blank_space = blank_space_percentage*length
        self.key_field_size = (length - self.blank_space*3)/4
        self._interval = self.key_field_size+self.blank_space
        self._bottom_padding = bottom_padding
        
        self.info = [length,screen_height,x,bottom_padding]
        self._keys = keys
        
        kf_x = [x,x+self._interval,x+self._interval*2,x+self._interval*3]
        kf_y = screen_height - bottom_padding

        # Sprites for the key fields   
        sprite = kf.MakeSprite.load_sprites("./assets/notes/keyfield/")
        screen = pg.display.get_surface()


        
        self.key_fields = [kf.KeyField(kf_x[0], kf_y, (255, 0, 0), (220, 0, 0), keys[0], sprite[0], size=self.key_field_size),
              kf.KeyField(kf_x[1], kf_y, (0, 255, 0), (0, 220, 0), keys[1], sprite[1], size=self.key_field_size), 
              kf.KeyField(kf_x[2], kf_y, (0, 0, 255), (0, 0, 220), keys[2], sprite[2], size=self.key_field_size), 
              kf.KeyField(kf_x[3], kf_y, (255, 255, 0), (220, 220, 0), keys[3], sprite[3],size=self.key_field_size),]
        self.make_background(screen)
        
        self.first_update = True
    def make_background(self, screen):
        """
        Creates and scales the background sprite for the playground.

        This function calculates the background rectangle based on the key fields,
        loads the background image, and scales it to fit the calculated rectangle.

        Parameters:
        screen (pygame.Surface): The display surface on which the background will be drawn.
        """
        self.background_rect = self.calc_background_rect(self.key_fields)
        self.background_sprite = pg.image.load("./assets/game_screen/barras.png").convert_alpha()
        self.background_sprite = pg.transform.scale(self.background_sprite, (self.background_rect.width, self.background_rect.height))
    def make_border(self, screen):
        """
        Creates and draws the border of the playground.

        This function calculates the border rectangles, loads the border images, and scales them to fit the calculated rectangles.

        Parameters:
        screen (pygame.Surface): The display surface on which the border will be drawn.
        """
        self.height = 5
        self.lower_rects = []
        self.side_left_rect = pg.Rect(self.background_rect.x, self.background_rect.top, self.height, self.background_rect.height)
        self.side_right_rect = pg.Rect(self.background_rect.right - self.height, self.background_rect.top, self.height, self.background_rect.height)

        # Desenha as laterais
        kf.MakeSprite(self.side_left_rect, "./assets/game_screen/line/side/side_left.png").draw(screen)
        kf.MakeSprite(self.side_right_rect, "./assets/game_screen/line/side/side_right.png").draw(screen)

        # Calcula e desenha os retângulos inferiores
        for i in range(4):
            x_pos = self.background_rect.x + i * self.background_rect.width // 4
            rect = pg.Rect(x_pos, self.background_rect.bottom - self.height, self.background_rect.width // 4, self.height)
            self.lower_rects.append(rect)

            # Ajusta e desenha o sprite
            sprite = pg.image.load(f"./assets/game_screen/line/lower/border_{i}.png").convert_alpha()
            scaled_sprite = pg.transform.scale(sprite, (rect.width, rect.height))
            screen.blit(scaled_sprite, rect.topleft)
    def update(self, screen, update_ratios, speed,screen_size=[480,640]):

        width_ratio = screen.get_width() / screen_size[1]
        height_ratio = screen.get_height() / screen_size[0]
        self._bottom_padding = self._bottom_padding*height_ratio
        self._interval = self._interval * width_ratio
        self.key_field_size = self.key_field_size * width_ratio
        bias = self.key_field_size*(1/6)

        x = self.info[2]*width_ratio
        y = screen.get_height() - self._bottom_padding - self.key_field_size
        for i in self.key_fields:
            i.bias = bias
            i.rect.x = x
            i.rect.y = y
<<<<<<< HEAD

            i.space_rect.x = x
            i.trian_rect.x = x
            i.shadow_sup_rect.x = x
            i.shadow_inf_rect.x = x
            i.shadow_sup_rect.y = y + y/50
            i.shadow_inf_rect.top = i.shadow_sup_rect.bottom
            
            x = x + self.interval
=======
            x = x + self._interval
>>>>>>> main
            
            i.rect.width = self.key_field_size
            i.rect.height = self.key_field_size

            i.space_rect.width = self.key_field_size
            i.space_rect.height = screen.get_height()
            i.trian_rect.width = self.key_field_size
            i.trian_rect.height = self.key_field_size
            i.shadow_sup_rect.width = self.key_field_size
            i.shadow_sup_rect.height = self.key_field_size // 2
            
            i.shadow_inf_rect.width = self.key_field_size
            i.shadow_inf_rect.height = screen.get_height() - i.shadow_sup_rect.bottom

        self.background_rect = self.calc_background_rect(self.key_fields)
        self.background_sprite = pg.transform.scale(
            pg.image.load("./assets/game_screen/barras.png").convert_alpha(),
            (self.background_rect.width, self.background_rect.height),
        )
        if width_ratio != 1:
            speed = speed / width_ratio
        
        update_ratios(width_ratio,height_ratio)
        self.info[2] = self.info[2]*width_ratio

        return ([screen.get_height(),screen.get_width()], speed)
    def draw(self, screen):
        """
        Draws the playground background on the given screen.

        Parameters:
        screen (pygame.Surface): The display surface on which the playground will be drawn.
        """
        screen.blit(self.background_sprite, (self.background_rect.x, self.background_rect.y))
    def get_rect(self):
        """
        Returns the rectangle of the playground background.

        Returns:
            pygame.Rect: The background rectangle of the playground.
        """
        return self.background_rect
    def calc_background_rect(self, keyfields: list):
        """
        Calculates the background rectangle of the playground based on the given keyfields.

        This function calculates the x and y coordinates of the background rectangle based on the positions of the first and last key fields.

        Parameters:
        keyfields (list): A list of keyfield objects.

        Returns:
            pygame.Rect: The background rectangle of the playground.
        """

        first_keyfield = keyfields[0]
        last_keyfield = keyfields[-1]
        
        x_start = first_keyfield.rect.x - 15
        x_end = last_keyfield.rect.x + last_keyfield.rect.width + 15
        
        screen_height = pg.display.get_surface().get_height()
        return pg.Rect(x_start, 0, x_end - x_start, screen_height)
        