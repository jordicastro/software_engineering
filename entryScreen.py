from typing import Callable
import pygame, sys

from database import Database
from server import Server
from player import Player
from gui import InputBox, InputLine, Button

class EntryScreen:
    def __init__(self, screen: pygame.Surface, db: Database, server: Server, get_players: Callable, check_player: Callable, add_player: Callable, start_action: Callable):
        self.db = db
        self.server = server
        pygame.init()
        self.screen = screen
        self.X = int(self.screen.get_width())
        self.Y = int(self.screen.get_height())
        self.red_lines: list[InputLine] = []
        self.green_lines: list[InputLine] = []
        self.input_boxes: list[InputBox] = []
        self.buttons: list[Button] = []
        self.adding = False
        self.get_players = get_players
        self.check_player = check_player
        self.add_player = add_player
        self.start_action = start_action

    # Render title
    def title(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        title = font.render('Edit Current Game', True, ("white"), ("black"))
        textRect = title.get_rect()
        textRect.center = (self.X // 2, textRect.bottom)
        return self.screen.blit(title, textRect)

    # Render text box
    def textBox(self, input: str, fontSize: int, color: str, x: int, y: int, bg: tuple):
        font = pygame.font.Font('freesansbold.ttf', fontSize)
        text = font.render(input, True, color, bg)
        textRect = text.get_rect()
        textRect.center = (x, y)
        return self.screen.blit(text, textRect)

    def background(self):
        # Initializing Color
        RED = (128, 23, 23)
        GREEN = (17, 122, 13)
        # Wiping after logo
        pygame.display.set_caption('Player Entry Screen')
        self.screen.fill("black")
        self.title()
        redX = self.X/2 - 100 - 400 - 100  # middle of screen, 100 left of box, 400 for width of boxes, 100 right of boxes
        redY = 75
        redW = 100+400+100            #100 left of box, 400 for width of boxes, 100 right of boxes
        redH = 800
        greenX = self.X/2
        greenY = 75
        greenW = 100 + 400 + 100
        greenH = 800
        # Setup player selection environment
        pygame.draw.rect(self.screen, RED, pygame.Rect(redX, redY, redW, redH))
        pygame.draw.rect(self.screen, GREEN, pygame.Rect(greenX, greenY, greenW, greenH))
        self.textBox("ID", 32, "white", redX+100+100, redY+30, RED)
        self.textBox("ID", 32, "white", greenX+100+100, greenY+30, GREEN)
        self.textBox("Name", 32, "white", redX+redW-100-100, redY+30, RED)
        self.textBox("Name", 32, "white", greenX+greenW-100-100, greenY+30, GREEN)
        # Labels for inputs
        self.textBox("Player ID:", 20, "white", self.X/2-100-100, self.Y/2+100+75+40, (128,23,23))
        self.textBox("Equipment ID:", 20, "white", self.X/2-100-100, self.Y/2+50+75+40, (128,23,23))

        if self.adding:
            self.textBox("Name:", 20, "white",  self.X/2-100-100, self.Y/2 + 40+75, (128,23,23))

    def render(self):
        # Render background
        self.background()
        # Get players
        red_players = self.get_players(True)
        green_players = self.get_players(False)
        # Draw player lines
        for i, line in enumerate(self.red_lines):
            if i < len(red_players):
                line.setPlayer(red_players[i])
            line.draw(self.screen)
        for i, line in enumerate(self.green_lines):
            if i < len(green_players):
                line.setPlayer(green_players[i])
            line.draw(self.screen)
        # Draw input boxes
        for i, box in enumerate(self.input_boxes):
            if i == 2 and not self.adding:
                continue
            box.draw(self.screen)
        # Draw buttons
        for button in self.buttons:
            button.process(self.screen)

    def events(self, event):
        for line in self.red_lines + self.green_lines:
            line.handle_event(event)
        for box in self.input_boxes:
            box.handle_event(event)

    # Initialize player lines
    def initPlayerLines(self, num_boxes: int):
        # Set up variables
        start = 128
        height = 32
        end = start + (height * num_boxes)
        # Create player lines for both teams
        for i in range(start, end, height):
            self.red_lines.append(InputLine(self.X/2-100-400, i, 200, height))
            self.green_lines.append(InputLine(self.X/2+100, i, 200, height))

    # Clear input boxes
    def clearBoxes(self):
        for box in self.input_boxes:
            box.clear()

    # Clear player lines
    def clearLines(self):
        for line in self.red_lines:
            line.clear()
        for line in self.green_lines:
            line.clear()

    # Add player to game
    def addPlayer(self, player: Player):
        ret = self.db.select(player.player_id)
        self.server.send_id(player.equip_id)
        self.adding = False
        adding_player = Player(player.player_id, ret['name'], player.equip_id, 0)
        self.add_player(adding_player)
        if player.team:
            self.red_lines[len(self.get_players(player.team)) - 1].setPlayer(adding_player)
        else:
            self.green_lines[len(self.get_players(player.team)) - 1].setPlayer(adding_player)
        self.clearBoxes()

    # Create player in database
    def createPlayer(self, player: Player):
        if player.player_id == '' or player.name == '' or player.equip_id == '':
            self.adding = True
            return False

        ret = self.db.insert(player.player_id, player.name)
        if ret:
            self.addPlayer(player)
        else:
            print("Error creating player")
        return ret

    def run(self):
        # Render background
        print("Rendering the Background")
        self.background()

        # Initialize player lines
        print("Initializing Player Lines")
        self.initPlayerLines(15)

        # Create input boxes
        print("Creating Input Boxes")
        self.id_field = InputBox(self.X/2-105, self.Y/2+100+75, 200, 32, True)
        self.input_boxes.append(self.id_field)
        self.equipment_field = InputBox(self.X/2-105, self.Y/2+50+75, 200, 32, True)
        self.input_boxes.append(self.equipment_field)
        self.name_field = InputBox(self.X/2-105, self.Y/2+75, 200, 32, True)
        self.input_boxes.append(self.name_field)

        def onAddPlayer():
            player = Player(int(self.id_field.text), self.name_field.text, int(self.equipment_field.text), 0)
            ret = self.check_player(player)
            if ret:
                # Check if player exists in database
                db_ret = self.db.check_id(player.player_id)
                if db_ret:
                    self.addPlayer(player)
                else:
                    self.createPlayer(player)
            else:
                print("Player or equipment already in game")

        # Create buttons
        print("Creating Buttons")
        self.buttons.append(Button(self.X/2-64, self.Y/2+200+10, 128, 32, onAddPlayer, 'Add Player'))
        self.buttons.append(Button(self.X/2-35, self.Y/2+250+10, 70, 32, self.start_action, 'Start'))

        print("Finished Entry Initialization")
