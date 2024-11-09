import pygame as pg

class Button:
    def __init__(self, x: float, y: float, width: float, height: float, text: str, font, color_normal, color_hover, text_color, texture_path=None):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.text_color = text_color
        self.hovered = False
        
        if texture_path:
            self.texture = pg.image.load(texture_path).convert_alpha()
            self.texture = pg.transform.scale(self.texture, (width, height))
        else:
            self.texture = None

    def draw(self, screen):
        if self.texture:
            screen.blit(self.texture, self.rect.topleft)
        else:
            color = self.color_hover if self.hovered else self.color_normal
            pg.draw.rect(screen, color, self.rect)

        if self.hovered and self.texture:
            hover_surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
            hover_surface.fill(self.color_hover)
            screen.blit(hover_surface, self.rect.topleft)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if self.hovered and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            pg.mixer.Sound('./assets/sounds/menu_select.wav').play()
            return True
        return False

class SetNotes:
    def __init__(self, screen, keys):
        self.screen = screen
        self.keys = keys
        self.previous_keys = keys.copy()
        self.buttons = []
        self.is_valid = False

        self.font = pg.font.Font("./assets/8bitoperator.ttf", 36)
        self.message_font = pg.font.Font("./assets/8bitoperator.ttf", 28)
        self.waiting_for_input = None

        filepath = "./assets/notes/keyfield/"
        font = pg.font.Font("./assets/8bitoperator.ttf", 20)
        color_normal = (0, 0, 255)
        hover_color = (0, 0, 255, 50)
        text_color = "white"
        
        for i, key in enumerate(keys):
            texture_path = filepath + f"botao_{i}.png"
            pos = ((SCREEN_WIDTH // 9) + 2 * i * SCREEN_WIDTH // 9, SCREEN_HEIGHT // 2)
            button = Button(pos[0], pos[1], SCREEN_WIDTH // 9, SCREEN_WIDTH // 9, key, font, color_normal, hover_color, text_color, texture_path)
            self.buttons.append(button)

    def check_repeat_keys(self):
        duplicate_keys = [key for key in self.keys if (self.keys.count(key) > 1)]
        
        if len(duplicate_keys) != 0:
            print(duplicate_keys)
            return True, duplicate_keys
        else: 
            return False, None
    def draw_error_message(self, duplicate_keys):
        error_message = "Teclas repetidas: " + ", ".join(set(duplicate_keys))
        error_text = self.message_font.render(error_message, True, (255, 0, 0))
        self.screen.blit(error_text, (SCREEN_WIDTH // 2 - error_text.get_width() // 2, SCREEN_HEIGHT - 50))

    def draw(self):
        self.screen.fill((255, 255, 255))
        title_text = self.message_font.render("Configuração das teclas:", True, (0, 0, 0))
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        
        has_repeats, duplicate_keys = self.check_repeat_keys()
        
        
        if has_repeats:
            self.draw_error_message(duplicate_keys)

        for i, button in enumerate(self.buttons):
            is_duplicate = self.keys.count(self.keys[i]) > 1
            text_color = (255, 0, 0) if is_duplicate else button.text_color
            text_surface = button.font.render(button.text, True, text_color)
            text_rect = text_surface.get_rect(center=button.rect.center)
            button.draw(self.screen)
            self.screen.blit(text_surface, text_rect)


    def on_event(self, event):
        if event.type == pg.KEYDOWN and self.waiting_for_input is not None:
            #new_key = pg.key.name(event.key)
            keys = pg.key.get_pressed()
            print(event.key)
            new_key = event.key
            
            self.keys[self.waiting_for_input] = new_key
            self.buttons[self.waiting_for_input].text = pg.key.name(new_key)
            self.waiting_for_input = None

            has_repeats, _ = self.check_repeat_keys()
            
            if has_repeats:
                self.keys = self.previous_keys.copy()
                print("Teclas repetidas detectadas. As alterações foram revertidas.")
                print("Teclas atuais:", self.keys)
            else:
                self.previous_keys = self.keys.copy()  # Atualiza o backup
                print("Teclas atualizadas:", self.keys)

        elif event.type == pg.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event):
                    self.waiting_for_input = i
                    break

    def check_hover(self, mouse_pos):
        for button in self.buttons:
            button.check_hover(mouse_pos)

# Inicializa o Pygame
pg.init()

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Configuração de Teclas")

# Define as teclas padrão
keys = ["d", "f", "j", "k"]
set_notes_screen = SetNotes(screen, keys)

# Loop principal
running = True
clock = pg.time.Clock()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        else:
            set_notes_screen.on_event(event)

    mouse_pos = pg.mouse.get_pos()
    set_notes_screen.check_hover(mouse_pos)
    pg.display.update()
    
    set_notes_screen.draw()

    clock.tick(60)

pg.quit()
