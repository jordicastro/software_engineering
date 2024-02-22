import socket
import json
# client's send_port = server's receive_port
SEND_PORT = 7501
BROADCAST_PORT = 7500
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
SEND_ADDR = (SERVER, SEND_PORT)
# client's listen_addr = server's broadcast_addr
LISTEN_ADDR = (SERVER, BROADCAST_PORT)

class Client:
    def __init__(self, SERVER='127.0.0.1', SEND_PORT=7501, BROADCAST_PORT=7500) -> None:
        self.SEND_ADDR = (SERVER, SEND_PORT)
        self.FORMAT = 'utf-8'
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        self.LISTEN_ADDR = (SERVER, BROADCAST_PORT)
        self.broadcast_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        #.bind(): listening for server traffic
        self.broadcast_socket.bind(LISTEN_ADDR)

    # send initial connection
    def send(self, msg):
        print('\t[INITIAL SEND]')
        message = msg.encode(self.FORMAT)
        self.socket.sendto(message, self.SEND_ADDR)

    # transmit equipment codes after each player addition
    def send_id(self, player_id): # sends id of newly created player & id of player hit
        # encoding id
        message = player_id.encode(self.FORMAT)
        # sending msg to server
        self.socket.sendto(message, self.SEND_ADDR)
    
    def send_hit_id(self, player_id, hit_id):
        message = f'{player_id}:{hit_id}'.encode(self.FORMAT)
        print(f'\t[SENDING IDs] Sending message {message} to Server')
        self.socket.sendto(message, self.SEND_ADDR)

    # def handle_server(self):
    #     # wait for server to return message
    #     data, addr = self.socket.recvfrom(1024)
    #     # decode msg
    #     msg = data.decode(FORMAT)
    #     print(f'[CLIENT] message from server: {msg}')
    
    def receive_broadcast(self): # TODO: while True: for continuous broadcast listening (async?)
        print('in receiving method')
        data, addr = self.broadcast_socket.recvfrom(1024)
        print(f'received data from broadcast socket : {data}')
        hit_id = data.decode(self.FORMAT)
        print(f'\t[RECEIVED SERVER BROADCASTS] player hit = {hit_id}')
        # TODO: handle hit_id
        

print('[START] client is starting...')   
player1 = Client()
player1.send('player1 establishing connection')
# -----
player1.send_hit_id(12, 14)
player1.receive_broadcast()
player1.socket.close()
player1.broadcast_socket.close()
print('[DONE]')
# ?loop through players array and close sockets
''' ? find player hit assuming a players array, each player contains instance of client class as attribute?
players : Player = []
players.append(player1, player2)

if isHit:
    for player in players:
        if (player.id == hit_id:
            player.client.send_hid_id(self.id, hit_id)
''' 