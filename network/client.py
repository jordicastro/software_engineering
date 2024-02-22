import socket
import json
# client's send_port = server's receive_port
SEND_PORT = 7501
BROADCAST_PORT = 7500
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
SEND_ADDR = (SERVER, SEND_PORT)
BROADCAST_ADDR = (SERVER, BROADCAST_PORT)

class Client:
    def __init__(self, SERVER='127.0.0.1', SEND_PORT=7501, BROADCAST_PORT=7500) -> None:
        self.SEND_ADDR = (SERVER, SEND_PORT)
        self.FORMAT = 'utf-8'
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        self.BROADCAST_ADDR = (SERVER, BROADCAST_PORT)
        self.broadcast_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # send initial connection
    def send(self, msg):
        message = msg.encode(self.FORMAT)
        self.socket.sendto(message, self.SEND_ADDR)

    # transmit equipment codes after each player addition
    def send_id(self, player_id): # sends id of newly created player & id of player hit
        # encoding id
        message = player_id.encode(self.FORMAT)
        # sending msg to server
        self.socket.sendto(message, self.SEND_ADDR)
    
    def send_hit_id(self, player_id, hit_id):
        message = {
            'player_id' : player_id,
            'hit_id' : hit_id,
            }
        print(f'message before json.dumps: {message}')
        json_msg = json.dumps(message) # json to string
        print(f'json msg: {json_msg}')
        message = json_msg.encode(self.FORMAT)
        print(f'encoded message {message}')
        self.socket.sendto(message, self.SEND_ADDR)

    # def handle_server(self):
    #     # wait for server to return message
    #     data, addr = self.socket.recvfrom(1024)
    #     # decode msg
    #     msg = data.decode(FORMAT)
    #     print(f'[CLIENT] message from server: {msg}')
    
    def receive_broadcast(self):
        data, addr = self.broadcast_socket.recvfrom(1024)

        hit_id = data.decode(FORMAT)
        print(f'[CLIENT] Server Broadcast: player hit = {hit_id}')
        

    
player1 = Client()
player1.send(' player1 establishing connection')
# -----
player1.send_id('0123456')

print('handling server response')
player1.handle_server()
player1.socket.close()
player1.broadcast_socket.close()
# loop through players array and close sockets
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