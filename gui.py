from typing import Callable
import pygame as pg
from player import Player

pg.init()
COLOR_INACTIVE = pg.Color('black')
COLOR_ACTIVE = pg.Color('white')
FONT = pg.font.Font(None, 32)

# User input box
class InputBox:
    def __init__(self, x: int, y: int, w: int, h: int, edit: bool = False, text: str = ''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.can_edit = edit

    def flip_active(self):
        self.active = not self.active
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

    def clear(self):
        self.text = ''

    def getActive(self):
        return self.active

    def getText(self):
        return self.text

    def handle_event(self, event: pg.event.Event):
        if self.can_edit:
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F12:
                    self.text = ''
                if self.active:
                    if event.key == pg.K_RETURN: #this will be where the code interfaces with server
                        print(self.text)
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pg.K_DELETE:
                        self.text = ""
                    else:
                        self.text += event.unicode
        # Re-render the text.
        self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen: pg.Surface):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

# User input line (two input boxes, one for ID and one for name)
class InputLine:
    def __init__(self, x: int, y: int, w: int, h: int, text: str = ''):
        self.id = InputBox(x, y, w, h)
        self.name = InputBox(x+w, y, w, h)
        self.input_line = [self.id, self.name]

    def getIDBox(self):
        return self.id

    def getNameBox(self):
        return self.name

    def getID(self):
        return self.id.text

    def getName(self):
        return self.name.text

    def setID(self, text: int):
        self.id.text = str(text)

    def setName(self, text: str):
        self.name.text = text

    def setPlayer(self, player_data: Player):
        self.id.text = str(player_data.player_id)
        self.name.text = player_data.name

    def clear(self):
        self.id.clear()
        self.name.clear()

    def draw(self, screen: pg.Surface):
        self.id.draw(screen)
        self.name.draw(screen)

    def handle_event(self, event: pg.event.Event):
        self.id.handle_event(event)
        self.name.handle_event(event)

# User input button
class Button():
    def __init__(self, x: int, y: int, width: int, height: int, onPress: Callable = None, text: str = 'Button', single: bool = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click_function = onPress
        self.one_press = single
        self.already_pressed = False
        self.text = text

        self.fill_colors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.surface = pg.Surface((self.width, self.height))
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.button_surf = FONT.render(text, True, (20, 20, 20))

    def getText(self):
        return self.text

    def setText(self, text: str):
        self.text = text
        self.button_surf = FONT.render(text, True, (20, 20, 20))

    def process(self, screen: pg.Surface):
        mousePos = pg.mouse.get_pos()
        self.surface.fill(self.fill_colors['normal'])
        if self.rect.collidepoint(mousePos):
            self.surface.fill(self.fill_colors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.surface.fill(self.fill_colors['pressed'])
                if self.one_press:
                    self.on_click_function()
                elif not self.already_pressed:
                    self.on_click_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False
        self.surface.blit(self.button_surf, [
            self.rect.width/2 - self.button_surf.get_rect().width/2,
            self.rect.height/2 - self.button_surf.get_rect().height/2
        ])
        screen.blit(self.surface, self.rect)