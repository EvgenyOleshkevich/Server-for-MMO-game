from main import *
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Timer
from constants import *
import uuid

Players = {}

def handleUpdate(data):
    0

active_users = set()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@socketio.on('generate_new_player')
def generate_new_player(data):
    uid = str(uuid.uuid4())
    Players[uid] = Player(uuid,
        data["x"] if data["x"] else 0, 
        data["y"] if data["y"] else 0,
        INITIAL_HP)
    active_users.add(uid)
    emit('uid', {
        "uid": uid
    })

@socketio.on('hit')
def test_message(message):
    print(message)
    emit('hit', {
        "data": hit(message["data"])
    })

@socketio.on('update')
def update(message):
    handleUpdate(message)
    if message.data:
        print(str(message.data))
    emit('update', message)

if __name__ == '__main__':
    print("Running server! Visit http://127.0.0.1:5000/ for api")
    socketio.run(app, host="0.0.0.0")