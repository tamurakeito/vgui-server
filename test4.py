import socketio
from socket import socket, AF_INET, SOCK_DGRAM

HOST = ''
PORT = 5000

sio = socketio.Client()

def on_connect():
    sio.emit('python', 'python socketio connect')

sio.on('connect', on_connect)
sio.connect('http://127.0.0.1:3001/')

# ソケットを用意
s = socket(AF_INET, SOCK_DGRAM)
# バインドしておく
s.bind((HOST, PORT))

while True:
    msg, address = s.recvfrom(8192)
    print(f"message: {msg}\nfrom: {address}")
    sio.emit('v-command', msg.decode())

s.close()
