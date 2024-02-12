import socket
import random
import time
from typing import List, Dict, Tuple, Optional

bufferSize = 1024
broadcastPort = 7500 # server is broadcasting
receivePort = 7501 # client receives 

serverAddress = ('127.0.0.1', broadcastPort) # tuple (server, port)
clientAddress = ('127.0.0.1', receivePort)

disconnect_message = '!DISCONNECT'

# Create datagram sockets
UDPServerSocketReceive = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocketTransmit = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# bind server socket
UDPServerSocketReceive.bind(serverAddress)
# connect client socket
UDPClientSocketTransmit.connect(clientAddress)

# final global vars
ADDPOINTS = 100

# player class
class Player:
    def __init__(self, equipment_id : str, codename : str, team_color : str, points : int=0) -> None:
        self.equipment_id = equipment_id
        self.codename = codename
        self.team_color = team_color
        self.points = points

    def updatePoints(self):
        self.points += ADDPOINTS

# players array
players = []

# add test players
player1 : Player = Player('010947283_id', 'jordinosaur', 'red', 0)
player2 : Player = Player('668348566_id', 'nicholasrex', 'green')

players.extend([player1], [player2])

def broadcast_code(code):
    UDPClientSocketTransmit.sendto(str(code).encode(), serverAddress)

def handle_received_data(data):
    print('handle_receieved_data')

def game_logic():
    print("Game start")
    broadcast_code(202)

# after game startdown counter, server transmits code 202 'accepted'
# Format of received (server -> clients) will be a single integer (equipment id of player who got hit)
received_data : str = ''
while received_data != '202':
    received_data, address = UDPServerSocketReceive.recvfrom(bufferSize)
    received_data = received_data.decode('utf-8')
    print ("Received from game software: " + received_data)

print('starting game:')

# the software will transmit code 221 three times when the game ends
counter = 0
while counter < 3:

    # Format of transmit data (client -> server) will be integer:integer (equipment id of player transmitting:equipment id of player hit)
    transmit_data : {str : str} = ''

    # code 43 : the green base has scored
        # increment greenbase score

    # code 53 : the red base has scored
        # increment redbase score
    
    # 
    if received_data != '221':
        counter+=1

    time.sleep(random.randint(1,3))

print('program complete.')