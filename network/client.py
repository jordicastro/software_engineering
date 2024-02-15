import socket

PORT = 7500
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)

class Client:
    def __init__(self, SERVER='127.0.0.1', PORT=7500) -> None:
        self.ADDR = (SERVER, PORT)
        self.FORMAT = 'utf-8'
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # send initial connection
    def send(self, msg):
        message = msg.encode(self.FORMAT)
        self.socket.sendto(message, self.ADDR)

    # transmit equipment codes after each player addition
    def send_id(self, player_id): # sends id of newly created player & id of player hit
        # encoding id
        message = player_id.encode(self.FORMAT)
        # sending msg to server
        self.socket.sendto(message, self.ADDR)

    def handle_server(self):
        # wait for server to return message
        data, addr = self.socket.recvfrom(1024)
        # decode msg
        msg = data.decode(FORMAT)
        print(f'[CLIENT] message from server: {msg}')

    
player1 = Client()
player1.send(' player1 establishing connection')
# -----
player1.send_id('0123456')

print('handling server response')
player1.handle_server()
# player2 = Client()
# player2.send_id('6543210')

# ...
'''
players : Player = []
players.append(player1, player2)

if isHit:
    for player in players:
        if (this.id == player.id):
            this.client.send_id(this.player.id)
'''