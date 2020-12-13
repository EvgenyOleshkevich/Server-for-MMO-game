from main import *
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Timer
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@socketio.on('hit')
def test_message(data):
    print(data)
    emit('hit', {
        data: hit(data)
    })

if __name__ == '__main__':
    socketio.run(app)