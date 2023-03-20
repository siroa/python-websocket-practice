from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# cors_allowed_originは今は適当
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/')
def index():
    return render_template('index.html')

# 接続
@socketio.on('connect')
def test_connect():
    emit('con', {'data': 'Connected'})

# message broadcast
@socketio.on('json')
def handle_receive(data):
    j_data = json.loads(data)
    room = j_data["room"]
    emit('receive', data, broadcast=True, to=room)

@socketio.on('join')
def on_join(data):
    print("join")
    j_data = json.loads(data)
    username = j_data['username']
    room = j_data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    print("leave")
    j_data = json.loads(data)
    username = j_data['username']
    room = j_data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)

if __name__ == '__main__':
    # デフォルトの開発用サーバーを使用
    socketio.run(app, debug=True)