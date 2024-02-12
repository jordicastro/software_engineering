import socket
from typing import List, Dict, Tuple, Optional

PORT = 7501
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)

class Client:
    def __init__(self, SERVER='127.0.0.1', PORT=7501) -> None:
        self.ADDR = (SERVER, PORT)
        self.FORMAT = 'utf-8'
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # self.client.connect(self.ADDR)

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        self.client.sendto(message, self.ADDR)

    # transmit equipment codes after each player addition
    def send_id(self, player_id): # sends id of newly created player & id of player hit
        message = player_id.encode(self.FORMAT)
        self.client.sendto(message, self.ADDR)

# client = Client()
# client.send('test')
        
player1 = Client()
player1.send_id('0123456')

player2 = Client()
player2.send_id('6543210')

# ...
'''
players : Player = []
players.append(player1, player2)

if isHit:
    for player in players:
        if (this.id == player.id):
            this.client.send_id(this.player.id)
'''