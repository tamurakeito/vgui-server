import sys
import socketio

sio = socketio.Client()
stdin = True

def on_connect():
    sio.emit('python', 'python socketio connect')

sio.on('connect', on_connect)
sio.connect('http://127.0.0.1:3001/')

while stdin:
    data = sys.stdin.readline()
    sio.emit('v-command', data)