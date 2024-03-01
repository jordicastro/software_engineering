from game import Game
from database import Database
import sys

# Create database object
db = Database()
# Create server object
server = None
# Create game object
game = Game(db, server)

# Run game
game.run()
