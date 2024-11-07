import pygame
import time

class Button:
    def __init__(self, x: float, y: float, width:float, height: float, text:str, font:str, color_normal, color_hover, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.text = text
        self.font = font
        self.text_color = text_color
        self.hovered = False

    def draw(self, screen):
        color = self.color_hover if self.hovered else self.color_normal
        pygame.draw.rect(screen, color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        # Verifica se o cursor está sobre o botão
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if self.hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True
        return False

class Welcome_screen():
    def __init__(self, size:tuple, running:bool, clock):
        self._size = size
        self._width, self._height = size
        self._running= running
        self.__clock = clock
        self.__screen = pygame.display.set_mode(self._size)
        self.__display = pygame.display.set_caption("OnBeat!!")
        self._8bitoperator_title = pygame.font.Font("./assets/8bitoperator.ttf", 40)
        self._8bitoperator_subtitle = pygame.font.Font("./assets/8bitoperator.ttf", 20)
        self._button_width, self._button_height = 220, 60
        self._bar_width, self._bar_height = 400, 25
        
    def execute(self):
        self.__display
        loading_message = self._8bitoperator_title.render("OnBeat!!", True, (255, 255, 255))

        dict_of_button = {}
        dict_of_button["button_start"] = Button(self._width//2 - self._button_width//4+70, self._height//2, self._button_width,\
                                                self._button_height,"Start", self._8bitoperator_title, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_settings"] = Button(self._width//2 - self._button_width-50, self._height//2, self._button_width,\
                                                   self._button_height,"Setings", self._8bitoperator_title, (255,255,255),(255,25,25), (0,0,0))

        running = True
        while running:
            self.__screen.fill((0, 0, 0))
            self.__screen.blit(loading_message, (self._width // 2 - loading_message.get_width() // 2, self._height // 2 - 100))
            for key in dict_of_button:
                dict_of_button[key].draw(self.__screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    for key in dict_of_button:
                        dict_of_button[key].check_hover(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_start"].is_clicked(event):
                    running = False 
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_settings"].is_clicked(event):
                    running = False 
                    return True
        pygame.time.Clock().tick(60)
    
    def run(self):
        pygame.init()
        while self.execute():
            settings = True
            while settings:
                option = self.seting_screen()
                if option in {1, 2, 3, 4}:
                    self.options(option)
                else:
                    settings = False
                if not self._running:
                    return False
        if not self._running:
            return False
        self.show_loading_screen()
        return True 
    
    def show_loading_screen(self):
        self.__screen
        self.__display
        
        loading_message = self._8bitoperator_subtitle.render("Carregando... Por favor, aguarde.", True, (255, 255, 255))

        self.__screen.fill((0, 0, 0))
        self.__screen.blit(loading_message, (self._width//2 - loading_message.get_width()//2, self._height//2 - 50))

        bar_width, bar_height = 400, 25  
        bar_x, bar_y = (self._width - bar_width) // 2, (self._height // 2) + 10  

        for i in range(bar_width):
            pygame.draw.rect(self.__screen, (255, 255, 255), (bar_x, bar_y, i, bar_height))
            pygame.display.flip()
            pygame.time.delay(5)

        time.sleep(2)

    def seting_screen(self):
        self.__screen
        self.__display
        loading_message = self._8bitoperator_subtitle.render(f"Number de algo = variavel", True, (255, 255, 255))
        loading_message2 = self._8bitoperator_subtitle.render(f"Number de algo = variavel", True, (255, 255, 255))
        loading_message3 = self._8bitoperator_subtitle.render(f"Number de algo = variavel", True, (255, 255, 255))

        button_width, button_height = 250, 60
        dict_of_button = {}

        dict_of_button["button_one"]=Button(self._width//2 - button_width//4+70, self._height//2 - 50, button_width, button_height,\
                          "o-o", self._8bitoperator_title, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_two"]=Button(self._width//2 - button_width-50, self._height//2 - 50, button_width, button_height,\
                          ":3", self._8bitoperator_title, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_three"]=Button(self._width//2 - button_width//4+70, self._height//2 +50, button_width, button_height,\
                          ":^", self._8bitoperator_title, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_back"]=Button(self._width//2 - button_width-50, self._height//2 +50, button_width, button_height,\
                          "back", self._8bitoperator_title, (255,255,255),(255,25,25), (0,0,0))
        self.clock = pygame.time.Clock()

        running = True
        while running:
            self.__screen.fill((0, 0, 0))
            for key in dict_of_button:
                dict_of_button[key].draw(self.__screen)
            self.__screen.blit(loading_message, (self._width // 2 - loading_message.get_width() // 2, self._height // 2 - 200))
            self.__screen.blit(loading_message2, (self._width // 2 - loading_message2.get_width() // 2, self._height // 2 - 150))
            self.__screen.blit(loading_message3, (self._width // 2 - loading_message3.get_width() // 2, self._height // 2 - 100))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    for key in dict_of_button:
                        dict_of_button[key].check_hover(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_one"].is_clicked(event):
                    running = False
                    return 1
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_two"].is_clicked(event):
                    running = False
                    return 2
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_three"].is_clicked(event):
                    running = False
                    return 3
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_back"].is_clicked(event):
                    running = False
                    return 0
        pygame.time.Clock().tick(30)   
    
    def options(self, option):
        self.__screen
        self.__display

        button_width, self.button_height = 250, 60
        dict_of_button = {}
        dict_of_button["button_easy"] = Button(self._width//2 - button_width-50, self._height//2 - 100, button_width, self.button_height,\
                          "Easy", self._8bitoperator_title, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_normal"] = Button(self._width//2 - button_width//4+70, self._height//2 - 100, button_width, self.button_height,\
                          "Normal", self._8bitoperator_title, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_hard"] = Button(self._width//2 - button_width-50, self._height//2, button_width, self.button_height,\
                          "Hard", self._8bitoperator_title, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_hardcore"] = Button(self._width//2 - button_width//4 +70, self._height//2, button_width, self.button_height,\
                          "Hardcore", self._8bitoperator_title, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_back"] = Button(self._width//2 - button_width + 100, self._height//2 + 100, button_width, self.button_height,\
                          "Back", self._8bitoperator_title, (255,255,255),(255,25,25), (0,0,0))
        self.clock = pygame.time.Clock()

        running = True
        while running:
            self.__screen.fill((0, 0, 0))
            for key in dict_of_button:
                dict_of_button[key].draw(self.__screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    for key in dict_of_button:
                        dict_of_button[key].check_hover(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_easy"].is_clicked(event):
                    if option == 1:
                        return
                    elif option == 2:
                        return
                    elif option == 3:
                        return
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_normal"].is_clicked(event):
                    if option == 1:
                        return
                    elif option == 2:
                        return
                    elif option == 3:
                        return
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_hard"].is_clicked(event):
                    if option == 1:
                        return
                    elif option == 2:
                        return
                    elif option == 3:
                        return
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_hardcore"].is_clicked(event):
                    if option == 1:
                        return
                    elif option == 2:
                        return
                    elif option == 3:
                        return
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_back"].is_clicked(event):
                    running = False
        pygame.time.Clock().tick(30)
        return 0