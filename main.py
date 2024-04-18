from game import Game
from database import Database
from server import Server

# Create database object
db = Database()
# Create server object
server = Server()
# Create game object
game = Game(db, server)

# Run game
game.run()
