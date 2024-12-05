import unittest
from unittest.mock import MagicMock
import pygame as pg
from src.screens import Button, MainMenu, Settings

class TestButton(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.screen = pg.Surface((800, 600))
        self.font = pg.font.Font(None, 36)  
        self.button = Button(x=100, y=100, width=200, height=50, text="Test", font=self.font)

    def tearDown(self):
        pg.quit()

    def test_initialization(self):
        """Testa se o botão é inicializado corretamente."""
        self.assertEqual(self.button.rect.x, 100)
        self.assertEqual(self.button.rect.y, 100)
        self.assertEqual(self.button.rect.width, 200)
        self.assertEqual(self.button.rect.height, 50)
        self.assertEqual(self.button.text, "Test")
        self.assertEqual(self.button.text_color, (255, 255, 255))
        self.assertFalse(self.button.hovered)
        self.assertIsNone(self.button.texture)

    def test_draw_without_texture(self):
        """Testa se o botão pode ser desenhado sem textura."""
        try:
            self.button.draw(self.screen)
        except Exception as e:
            self.fail(f"Falha ao desenhar botão sem textura: {e}")

    def test_draw_with_texture(self):
        """Testa se o botão pode ser desenhado com textura."""
        self.button.texture_path = "./assets/notes/keyfield/"
        try:
            self.button.draw(self.screen)
        except Exception as e:
            self.fail(f"Falha ao desenhar botão com textura: {e}")

    def test_hover_detection(self):
        """Testa se o botão detecta corretamente quando está com hover."""
        mouse_pos = (150, 120)  # Dentro do botão
        self.button._Button__check_hover(mouse_pos) 
        self.assertTrue(self.button.hovered)

        mouse_pos = (50, 50)  # Fora do botão
        self.button._Button__check_hover(mouse_pos)
        self.assertFalse(self.button.hovered)

    def test_is_clicked(self):
        """Testa se o botão detecta cliques corretamente."""
        # Simula movimento do mouse sobre o botão
        event_hover = pg.event.Event(pg.MOUSEMOTION, {"pos": (150, 120)})
        self.button.is_clicked(event_hover)
        self.assertTrue(self.button.hovered)

        # Simula clique do mouse sobre o botão
        event_click = pg.event.Event(pg.MOUSEBUTTONDOWN, {"pos": (150, 120), "button": 1})
        clicked = self.button.is_clicked(event_click)
        self.assertTrue(clicked)


class TestMainMenu(unittest.TestCase):
    def setUp(self):
        """Inicializa os testes."""
        pg.init()
        self.screen = pg.Surface((800, 600))
        self.manager = MagicMock()
        self.manager.language = "English"
        self.manager.is_running = True
        self.manager.change_state = MagicMock()
        
        # Inicializa o menu principal
        self.main_menu = MainMenu(button_width=200, button_height=50, manager=self.manager)

    def tearDown(self):
        """Finaliza os testes."""
        pg.quit()

    def test_initialization(self):
        """Testa a inicialização do menu principal."""
        self.assertEqual(len(self.main_menu.dict_buttons), 5)
        self.assertIn("start", self.main_menu.dict_buttons)
        self.assertIn("settings", self.main_menu.dict_buttons)
        self.assertIn("ModDev", self.main_menu.dict_buttons)
        self.assertIn("Help", self.main_menu.dict_buttons)
        self.assertIn("Exit", self.main_menu.dict_buttons)

    def test_resize(self):
        """Testa o método de redimensionamento."""
        self.main_menu.resize(self.screen)
        start_button = self.main_menu.dict_buttons["start"]
        self.assertEqual(start_button.rect.x, (self.screen.get_width() - self.main_menu.button_width) // 2)
        self.assertEqual(start_button.rect.y, (self.screen.get_height() // 9) + 120)

    def test_update_buttons(self):
        """Testa se os textos dos botões são atualizados corretamente."""
        new_labels = ["Start", "Settings", "DevMode", "Help", "Exit"]
        self.main_menu.translate = MagicMock(return_value=new_labels)
        self.main_menu.update(self.screen)

        self.assertEqual(self.main_menu.dict_buttons["start"].text, "Start")
        self.assertEqual(self.main_menu.dict_buttons["settings"].text, "Settings")
        self.assertEqual(self.main_menu.dict_buttons["ModDev"].text, "DevMode")
        self.assertEqual(self.main_menu.dict_buttons["Help"].text, "Help")
        self.assertEqual(self.main_menu.dict_buttons["Exit"].text, "Exit")

    def test_on_event_start_game(self):
        """Testa se o método `on_event` chama a ação correta ao clicar nos botões."""
        start_event = pg.event.Event(pg.MOUSEBUTTONDOWN, {"pos": (150, 130), "button": 1})
        self.main_menu.dict_buttons["start"].is_clicked = MagicMock(return_value=True)
        self.main_menu.on_event(start_event, self.screen)

        self.manager.change_state.assert_called_once_with("music_catalog")

    def test_exit_button(self):
        """Testa se o botão de saída encerra o jogo."""
        exit_event = pg.event.Event(pg.MOUSEBUTTONDOWN, {"pos": (150, 130), "button": 1})
        self.main_menu.dict_buttons["Exit"].is_clicked = MagicMock(return_value=True)
        self.main_menu.on_event(exit_event, self.screen)

        self.assertFalse(self.manager.is_running)

class TestSettings(unittest.TestCase):
    def setUp(self):
        """Configura o ambiente para os testes."""
        pg.init()
        self.screen = pg.Surface((800, 600))
        self.manager = MagicMock()
        self.manager.language = "English"
        self.manager.change_state = MagicMock()

        # Inicializa o menu de configurações
        self.settings = Settings(button_width=200, button_height=50, manager=self.manager)

    def tearDown(self):
        """Finaliza o ambiente após os testes."""
        pg.quit()

    def test_initialization(self):
        """Testa se os botões foram inicializados corretamente."""
        self.assertEqual(len(self.settings.dict_buttons), 3)
        self.assertIn("language", self.settings.dict_buttons)
        self.assertIn("keys", self.settings.dict_buttons)
        self.assertIn("back", self.settings.dict_buttons)

    def test_resize(self):
        """Testa o redimensionamento dos botões."""
        self.settings.resize(self.screen)
        language_button = self.settings.dict_buttons["language"]
        self.assertEqual(language_button.rect.x, (self.screen.get_width() - self.settings.button_width) // 2)
        self.assertEqual(language_button.rect.y, (self.screen.get_height() // 9) + 120)

        back_button = self.settings.dict_buttons["back"]
        self.assertEqual(back_button.rect.x, (self.screen.get_width() - self.settings.button_width) // 2)
        self.assertEqual(back_button.rect.y, (self.screen.get_height() // 9) + 2 * (self.settings.button_height + 10) + 120)

    def test_update_buttons(self):
        """Testa se os textos dos botões são atualizados corretamente."""
        new_labels = ["Idioma", "Teclas", "Voltar"]
        self.settings.translate = MagicMock(return_value=new_labels)
        self.settings.update(self.screen)

        self.assertEqual(self.settings.dict_buttons["language"].text, "Idioma")
        self.assertEqual(self.settings.dict_buttons["keys"].text, "Teclas")
        self.assertEqual(self.settings.dict_buttons["back"].text, "Voltar")

    def test_on_event_keys(self):
        """Testa se o botão 'keys' altera para o estado correto."""
        self.settings.dict_buttons["keys"].is_clicked = MagicMock(return_value=True)
        event = pg.event.Event(pg.MOUSEBUTTONDOWN, {"pos": (150, 130), "button": 1})

        self.settings.on_event(event, self.screen)
        self.manager.change_state.assert_called_once_with("key")

    def test_on_event_back(self):
        """Testa se o botão 'back' retorna ao menu principal."""
        self.settings.dict_buttons["back"].is_clicked = MagicMock(return_value=True)
        event = pg.event.Event(pg.MOUSEBUTTONDOWN, {"pos": (150, 130), "button": 1})

        self.settings.on_event(event, self.screen)
        self.manager.change_state.assert_called_once_with("main_menu")

if __name__ == "__main__":
    unittest.main()
