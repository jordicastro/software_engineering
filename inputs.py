import pygame as pg
pg.init()
COLOR_INACTIVE = pg.Color('black')
COLOR_ACTIVE = pg.Color('white')
FONT = pg.font.Font(None, 32)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        
    def flip_active(self):
        self.active = not self.active
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
    def clear(self):
        self.text = ''
    def handle_event(self, event):
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
                elif event.key == pg.K_TAB:
                    self.active = False
                    self.color = COLOR_INACTIVE
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        # pg.draw.rect(screen, 'black', pg.draw.rect(screen, self.color, self.rect, 2))
        pg.draw.rect(screen, self.color, self.rect, 2)