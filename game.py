from database import Database
from server import Server
from player import Player
from splash import splashScreen
#from actionScreen import ActionScreen
from entryScreen import EntryScreen
import pygame, sys

# Game class
class Game:
    # Initialize game
    def __init__(self, db: Database, server: Server):
        self.db = db
        self.server = server
        pygame.init()
        # Window setup
        self.desktop = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.desktop.current_w-10, self.desktop.current_h-50))
        self.clock = pygame.time.Clock()
        self.X = int(self.screen.get_width())
        self.Y = int(self.screen.get_height())
        # Variable creation
        self.red_players: list[Player] = []
        self.green_players: list[Player] = []
        self.running: bool = True
        self.page: str = 'entry'

    def startGame(self):
        print("Starting Game")
        self.page = 'action'

    # Handling events function
    def events(self):
        for event in pygame.event.get():
            if self.page == 'entry':
                self.entry_screen.events(event)
            elif self.page == 'action':
                #self.action_screen.events(event)
                pass
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
                    self.entry_screen.clearLines()
                # F5 key switches to action screen
                if event.key == pygame.K_F5:
                    self.startGame()

    # Render elements
    def render(self):
        if self.page == 'entry':
            self.entry_screen.render()
        elif self.page == 'action':
            #self.action_screen.render()
            pass

    # Return players of a given team
    def getPlayers(self, team: bool):
        if team:
            return self.red_players
        else:
            return self.green_players

    # Run main game
    def run(self):
        # Splash screen
        splashScreen()

        # Check if player exists in game already
        def checkPlayer(player: Player) -> bool:
            for existing in self.red_players + self.green_players:
                if existing.player_id == player.player_id:
                    return False
                if existing.equip_id == player.equip_id:
                    return False
            return True

        def addPlayer(player: Player):
            if player.team:
                self.red_players.append(player)
            else:
                self.green_players.append(player)

        # Entry screen
        self.screen = pygame.display.set_mode((self.X, self.Y))
        self.entry_screen = EntryScreen(self.screen, self.db, self.server, self.getPlayers, checkPlayer, addPlayer, self.startGame)
        self.entry_screen.run()

        # Main game loop
        print("Running Game")
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