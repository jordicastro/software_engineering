import pygame as pg
from player import Player

pg.init()
COLOR_INACTIVE = pg.Color('black')
COLOR_ACTIVE = pg.Color('white')
FONT = pg.font.Font(None, 32)
BUTTON_HOVER_COLOR = '#666666'
BUTTON_COLOR = '#ffffff'
# User input box
class InputBox:
    def __init__(self, x, y, w, h, edit=False, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.canEdit = edit

    def flip_active(self):
        self.active = not self.active
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
    def clear(self):
        self.text = ''
    def getActive(self):
        return self.active
    def getText(self):
        return self.text
    def handle_event(self, event):
        if self.canEdit:
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
                        self.text = self.text
                    elif event.key == pg.K_DELETE:
                        self.text = ""
                    else:
                        self.text += event.unicode
        # Re-render the text.
        self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self): #Don't currently need
        # Resize the box if the text is too long.
        #width = max(200, self.txt_surface.get_width()+10)
        #self.rect.w = width
        return
    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

# User input line (two input boxes, one for ID and one for name)
class InputLine:
    def __init__(self, x, y, w, h, text=''):
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
    def setID(self, text):
        self.id.text = str(text)
    def setName(self, text):
        self.name.text = text
    def setPlayer(self, player_data: Player):
        self.id.text = str(player_data.player_id)
        self.name.text = player_data.name
    def clear(self):
        self.id.clear()
        self.name.clear()
    def draw(self, screen):
        self.id.draw(screen)
        self.name.draw(screen)
    def handle_event(self, event):
        self.id.handle_event(event)
        self.name.handle_event(event)

# User input button
class Button():
    def __init__(self, x, y, width, height, onclickFunction=None, buttonText='Button', onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.text = buttonText

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pg.Surface((self.width, self.height))
        self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = FONT.render(buttonText, True, (20, 20, 20))
    def getText(self):
        return self.text
    def setText(self, text):
        self.text = text
        self.buttonSurf = FONT.render(text, True, (20, 20, 20))
    def draw(self, screen):
        mousePos = pg.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)