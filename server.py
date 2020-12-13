from main import *
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Timer
import uuid

active_users = set()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@socketio.on('get_uid')
def generate_uid():
    uid = str(uuid.uuid4())
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
    result = {}
    if message.data:
        print(message.data)
    emit('update', result)

if __name__ == '__main__':
    print("Running server! Visit http://127.0.0.1:5000/ for api")
    socketio.run(app, host="0.0.0.0")