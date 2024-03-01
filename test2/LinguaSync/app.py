from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join_room')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('announce_message', {'message': f'{username} has joined the room {room}.'}, room=room)

@socketio.on('leave_room')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('announce_message', {'message': f'{username} has left the room.'}, room=room)

@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    emit('announce_message', {'message': data['message']}, room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')

