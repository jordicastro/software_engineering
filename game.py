from database import Database
from server import Server
from player import Player
from splash import splashScreen
from gui import InputBox, InputLine, Button
from actionScreen import runGame
import pygame, sys

# Game class
class Game:
    # Initialize game
    def __init__(self, db: Database, server: Server):
        # Window setup
        self.db = db
        self.server = server
        pygame.init()
        self.desktop = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.desktop.current_w-10, self.desktop.current_h-50))
        self.clock = pygame.time.Clock()
        self.X = int(self.screen.get_width())
        self.Y = int(self.screen.get_height())
        # Variable creation
        self.red_players: list[Player] = []
        self.green_players: list[Player] = []
        self.red_lines: list[InputLine] = []
        self.green_lines: list[InputLine] = []
        self.input_boxes: list[InputBox] = []
        self.buttons: list[Button] = []
        self.running: bool = True
        self.adding: bool = False

    # Handling events function
    def events(self):
        for event in pygame.event.get():
            # Handle events for each player line and input box
            for line in self.red_lines + self.green_lines:
                line.handle_event(event)
            for input in self.input_boxes:
                input.handle_event(event)
            # If pygame quits, close the database and exit the program
            if event.type == pygame.QUIT:
                pygame.quit()
                self.db.close()
                self.server.stop()
                sys.exit()
            # Check for key presses
            elif event.type == pygame.KEYDOWN:
                # Escape key closes the program
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # F11 key toggles fullscreen
                if event.key == pygame.K_F11:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        pygame.display.set_mode((self.X, self.Y))
                    else:
                        pygame.display.set_mode((self.X, self.Y), pygame.FULLSCREEN)
                # F12 clears all players from the game
                if event.key == pygame.K_F12:
                    self.red_players = []
                    self.green_players = []
                    for line in self.red_lines + self.green_lines:
                        line.clear()
                if event.key == pygame.K_F5:
                    self.onStartHelper()

    # Render elements
    def render(self):
        # Render background
        self.background()
        # Draw player lines
        for i, line in enumerate(self.red_lines):
            if i < len(self.red_players):
                line.setPlayer(self.red_players[i])
            line.draw(self.screen)
        for i, line in enumerate(self.green_lines):
            if i < len(self.green_players):
                line.setPlayer(self.green_players[i])
            line.draw(self.screen)
        # Draw input boxes
        for i, box in enumerate(self.input_boxes):
            if i == 2 and not self.adding:
                continue
            box.draw(self.screen)
        # Draw buttons
        for button in self.buttons:
            button.process(self.screen)

    # Render title
    def title(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        title = font.render('Edit Current Game', True, ("white"), ("black"))
        textRect = title.get_rect()
        textRect.center = (self.X // 2, textRect.bottom)
        return self.screen.blit(title, textRect)

    # Render text box
    def textBox(self, input, fontSize: int, color, x, y, bg):
        font = pygame.font.Font('freesansbold.ttf', fontSize)
        text = font.render(input, True, (color), (bg))
        textRect = text.get_rect()
        textRect.center = (x, y)
        return self.screen.blit(text, textRect)

    # Render background
    def background(self):
        # Initializing Color
        RED = (128, 23, 23)
        GREEN = (17, 122, 13)
        # Wiping after logo
        pygame.display.set_caption('Player Selection')
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
        self.textBox("Player ID:", 20, "white", self.X/2-100-100, self.Y/2 + 40+75, (128,23,23))
        self.textBox("Equipment ID:", 20, "white", self.X/2-100-100, self.Y/2+50+40+75, (128,23,23))
        if self.adding:
            self.textBox("Name:", 20, "white",  self.X/2-100-100, self.Y/2 + 40+75, (128,23,23))

    # Initialize player lines
    def initPlayerLines(self, num_boxes):
        # Set up variables
        start = 128
        height = 32
        end = start + (height * num_boxes)
        # Create player lines for both teams
        for i in range(start, end, height):
            self.red_lines.append(InputLine(self.X/2-100-400, i, 200, height))
            self.green_lines.append(InputLine(self.X/2+100, i, 200, height))

    # Add player to game
    def addPlayer(self, player: Player):
        ret = self.db.select(player.player_id)
        self.server.send_id(player.equip_id)
        self.adding = False
        adding_player = Player(player.player_id, ret['name'], player.equip_id, 0)
        if player.team:
            self.red_players.append(adding_player)
            self.red_lines[len(self.red_players) - 1].setPlayer(adding_player)
        else:
            self.green_players.append(adding_player)
            self.green_lines[len(self.green_players) - 1].setPlayer(adding_player)
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

    def onStartHelper(self):
        print("Starting game")
        print(self.red_players)
        print(self.green_players)
        runGame(self.red_players,self.green_players, self.server)

    def clearBoxes(self):
        for box in self.input_boxes:
            box.clear()

    # Run main game
    def run(self):
        # Splash screen
        splashScreen()

        # Reinitialize screen size
        self.screen = pygame.display.set_mode((self.desktop.current_w, self.desktop.current_h))
        X = int(self.screen.get_width())
        Y = int(self.screen.get_height())
        # Render background
        self.background()

        # Initialize player lines
        self.initPlayerLines(15)

        # Create input boxes
        self.id_field = InputBox(X/2-105, Y/2+100+75, 200, 32, True)
        self.input_boxes.append(self.id_field)
        self.equipment_field = InputBox(X/2-105, Y/2+50+75, 200, 32, True)
        self.input_boxes.append(self.equipment_field)
        self.name_field = InputBox(X/2-105, Y/2+75, 200, 32, True)
        self.input_boxes.append(self.name_field)

        # Check if player exists in database and decide whether to add or create player
        def checkPlayer():
            # Encode player data
            player = Player(int(self.id_field.text), self.name_field.text, int(self.equipment_field.text), 0)
            # Check if player or equipment already exists in game
            for existing in self.red_players + self.green_players:
                if existing.player_id == player.player_id:
                    print("Player already exists in game")
                    self.clearBoxes()
                    return
                if existing.equip_id == player.equip_id:
                    print("Equipment already exists in game")
                    self.clearBoxes()
                    return
            # Check if player exists in database
            ret = self.db.check_id(player.player_id)
            if ret:
                # If player is found, add player to game
                self.addPlayer(player)
            else:
                # If not found, create player in database and then add to game
                self.createPlayer(player)

        # Start game
        def onStart():
            self.onStartHelper()

        # Create buttons
        addPlayerButton = Button(X/2-64, Y/2+200+10, 128, 32, checkPlayer, 'Add Player')
        self.buttons.append(addPlayerButton)
        startGameButton = Button(X/2-35, Y/2+250+10, 70, 32, onStart, 'Start')
        self.buttons.append(startGameButton)

        # Main game loop
        while self.running:
            # Handle events and render game window
            self.events()
            self.render()
            pygame.display.update()
            self.clock.tick(60) # 60 FPS

        # Quit game
        pygame.quit()
        self.db.close()
        self.server.stop()
        sys.exit()