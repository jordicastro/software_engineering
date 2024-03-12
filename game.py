from splash import splashScreen
from countdown import countdown
from gui import *
import pygame, sys, socket

# Game class
class Game:
    # Initialize game
    def __init__(self, db, server):
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
        self.red_players = []
        self.green_players = []
        self.red_lines = []
        self.green_lines = []
        self.input_boxes = []
        self.buttons = []

    # Handling events function
    def events(self):
        for event in pygame.event.get():
            # Handle events for each player line and input box
            for i, line in enumerate(self.red_lines + self.green_lines):
                line.handle_event(event)
            for i, input in enumerate(self.input_boxes):
                input.handle_event(event)
            # If pygame quits, close the database and exit the program
            if event.type == pygame.QUIT:
                pygame.quit()
                self.db.close()
                sys.exit()
            # Check for key presses
            elif event.type == pygame.KEYDOWN:
                # Escape key closes the program
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    pygame.quit()
                    self.db.close()
                    sys.exit()
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

    # Render elements
    def render(self):
        # Render background
        self.background()
        # Update player lines
        for player in self.red_players:
            self.red_lines[self.red_players.index(player)].setPlayer(player)
        for player in self.green_players:
            self.green_lines[self.green_players.index(player)].setPlayer(player)
        # Draw player lines
        for line in self.red_lines:
            line.draw(self.screen)
        for line in self.green_lines:
            line.draw(self.screen)
        # Draw input boxes
        for box in self.input_boxes:
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
    def textBox(self, input, color, x, y, bg):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(input, True, (color), (bg))
        textRect = text.get_rect()
        textRect.center = (x, y)
        return self.screen.blit(text, textRect)

    #calculate percentage values for screen
    def getDisplayPercent(self, percent):
        xOnePercent = int(self.X / 100)
        yOnePercent = int(self.Y / 100)
        xActualPercent = int(percent * xOnePercent)
        yActualPercent = int(percent * yOnePercent)
        point = dict()
        point['X'] = xActualPercent
        point['Y'] = yActualPercent
        return point
    
    # Render background
    def background(self):
        # Initializing Color
        RED = (128, 23, 23)
        GREEN = (17, 122, 13)
        # Wiping after logo
        pygame.display.set_caption('Player Selection')
        self.screen.fill("black")
        self.title()
        
        halfX = self.getDisplayPercent(50).get('X')
        widthValue = self.getDisplayPercent(32).get('X')
        yValue = self.getDisplayPercent(7).get('Y')
        heightValue = self.getDisplayPercent(70).get('Y')
        
        redX = halfX - widthValue # middle of screen, 100 left of box, 400 for width of boxes, 100 right of boxes
        redY = yValue
        redW = widthValue          #100 left of box, 400 for width of boxes, 100 right of boxes
        redH = heightValue
        
        greenX = halfX
        greenY = yValue
        greenW = widthValue
        greenH = heightValue
        
        textX = self.getDisplayPercent(10).get('X')
        textY = self.getDisplayPercent(3).get('Y')
        
        # Setup player selection environment
        pygame.draw.rect(self.screen, RED, pygame.Rect(redX, redY, redW, redH))
        pygame.draw.rect(self.screen, GREEN, pygame.Rect(greenX, greenY, greenW, greenH))
        self.textBox("ID", "white", redX+textX, redY+textY, RED)
        self.textBox("ID", "white", greenX+textX, greenY+textY, GREEN)
        self.textBox("Name", "white", redX+redW-textX, redY+textY, RED)
        self.textBox("Name", "white", greenX+greenW-textX, greenY+textY, GREEN)

    
    
    
    # Initialize player lines
    def initPlayerLines(self, num_boxes):
        # Set up variables
        start = self.getDisplayPercent(7).get('X')
        height = self.getDisplayPercent(3).get('Y')
        end = start + (height * num_boxes)
        # Create player lines for both teams
        midScreenX = self.getDisplayPercent(50).get('X')
        width = self.getDisplayPercent(11).get('X')
        redXOffset = midScreenX - width*2 - self.getDisplayPercent(5).get('X')
        greenXOffset = midScreenX + self.getDisplayPercent(5).get('X')
        for i in range(start, end, height):
            self.red_lines.append(InputLine(redXOffset, i, width, height))
            self.green_lines.append(InputLine(greenXOffset, i, width, height))

    # Encode player data to json
    def encodePlayer(self, player_id, name, equip_id):
        return {'player_id': int(player_id), 'name': name, 'equip_id': int(equip_id)}

    # Add player to game
    def addPlayer(self, player_id, equip_id):
        ret = self.db.select(player_id)
        if equip_id % 2 != 0:
            self.red_players.append(ret)
        else:
            self.green_players.append(ret)

    # Create player in database
    def createPlayer(self, player_id, name, equip_id):
        ret = self.db.insert(player_id, name)
        if ret:
            self.addPlayer(player_id, equip_id)
        else:
            print("Error creating player")
        return ret

    # Run main game
    def run(self):
        self.running = True

        # Splash screen
        splashScreen()

        # Reinitalize screen size
        self.screen = pygame.display.set_mode((self.desktop.current_w, self.desktop.current_h))
        X = int(self.screen.get_width())
        Y = int(self.screen.get_height())
        # Render background
        self.background()

        # Initialize player lines
        self.initPlayerLines(15)

        # Create input boxes
        
        idField = InputBox(X/2-110, Y/2+150, 200, 32, True)
        self.input_boxes.append(idField)
        equipmentField = InputBox(X/2-110, Y/2+100, 200, 32, True)
        self.input_boxes.append(equipmentField)
        nameField = InputBox(X/2-110, Y/2+50, 200, 32, True)
        self.input_boxes.append(nameField)

        # Check if player exists in database and decide whether to add or create player
        def checkPlayer():
            # Encode player data
            player = self.encodePlayer(idField.text, nameField.text, equipmentField.text)
            # Check if player exists in database
            ret = self.db.check_id(player['player_id'])
            if ret:
                # If player is found, add player to game
                self.addPlayer(player["player_id"], player["equip_id"])
            else:
                # If not found, create player in database and then add to game
                self.createPlayer(player["player_id"], player["name"], player["equip_id"])

        # Start game
        def onStart():
            countdown()
            print("Starting game")

        # Create buttons
        addPlayerButton = Button(X/2-64, Y/2+200, 128, 32, checkPlayer, 'Add Player')
        self.buttons.append(addPlayerButton)
        startGameButton = Button(X/2-35, Y/2+250, 70, 32, onStart, 'Start')
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
        sys.exit()