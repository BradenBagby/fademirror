import socket

from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, send, emit

from lib.fadecontroller import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
socketio = SocketIO(app)

fadeController = FadeCandyController()

@app.route('/')
def handle_get_index():
    return render_template('index.html')

@app.route('/thumb-control')
def handle_get_thumb_control():
    return render_template('thumb-control.html')

@app.route('/presets')
def handle_get_presets():
    return render_template('presets.html')

@socketio.on('connected')
def handle_connected_event(json):
    print('[+] client websocket connected')
    emit_ack('connected ack')

@socketio.on('xy')
def handle_xy_event(json):
    fadeController.printStatus()
    emit_ack('xy message ack')

@socketio.on('thumb_control')
def handle_thumb_control_event(json): 
    print(json)
    fadeController.printStatus()
    emit_ack('thumb_event ack')

def emit_ack(data):
    emit('ack', data)

if __name__ == '__main__':
    print('Starting server!')
    socketio.run(app, host='0.0.0.0', port=5000)