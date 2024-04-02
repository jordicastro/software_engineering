import socket, threading

RECEIVE_PORT = 7501
BROADCAST_PORT = 7500
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
RECEIVE_ADDR = (SERVER, RECEIVE_PORT)
BROADCAST_ADDR = (SERVER, BROADCAST_PORT)

class Server():
    def __init__(self):
        self.server_recv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_recv.bind(RECEIVE_ADDR)
        self.server_broadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_thread = threading.Thread(target=self.start)
        self.server_thread.start()

    def start(self):
        print(f'[LISTENING] server is listening on {self.server_recv}')

        # start listening for new connections
        while True:
            data, addr = self.server_recv.recvfrom(1024)
            if data:
                print(f'[CONNECTION] connection from {addr} received.')
                # decode data
                equip_id = data.decode(FORMAT)
                print(f'\t[BROADCASTING] data {equip_id} received. broadcasting to clients...')

                # send info to handle_client using threads
                client_thread = threading.Thread(target=self.handle_client(equip_id))
                client_thread.start()

    def stop(self):
        self.server_recv.close()
        self.server_broadcast.close()

    def handle_client(self, msg:str): # receive dictionary (int : int) on port 7501, send back broadcast (int) on port 7500
        if(':' in msg):
            try:
                transmit_id = int(msg.split(':')[0])
                hit_id = int(msg.split(':')[1])
            except ValueError:
                print('Invalid message format. Expected: player_id:hit_id')

            print(f'\t[BROADCASTING] hit_id {hit_id}, transmit_id {transmit_id} received. broadcasting to clients...')
            self.server_broadcast.sendto(str(hit_id).encode(FORMAT), BROADCAST_ADDR)
        else:
            print(f'\t[BROADCASTING] msg {msg} received and joined. broadcasting to clients...')
            self.server_broadcast.sendto(str(msg).encode(FORMAT), BROADCAST_ADDR)



    def add_player(self, player_id: int) -> None:
        self.server_broadcast.sendto(str(player_id).encode(FORMAT), BROADCAST_ADDR)

    # transmit equipment codes after each player addition
    def send_id(self, equip_id): # sends id of newly created player & id of player hit
        # sending msg to server
        client_thread = threading.Thread(target=self.handle_client(str(equip_id)))
        client_thread.start()

    # This can be used to send the hit id to the server
    # This is used for testing purposes
    def send_hit_id(self, equip_id, hit_id):
        #handle friendly fire:
        if equip_id % 2 == 0 and hit_id % 2 == 0 or equip_id % 2 == 1 and hit_id % 2 == 1:
            print(f'[FRIENDLY FIRE] transmitting self id')
            message = f'{equip_id}:{equip_id}'.encode(FORMAT)
        else:
            message = f'{equip_id}:{hit_id}'.encode(FORMAT)
        print(f'\t[SENDING IDs] Sending message {message} to Server')
        self.server_broadcast.sendto(message, BROADCAST_ADDR)
