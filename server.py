from main import *
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Timer
from constants import *
import json
import uuid

Players = {}
PlayersEvents = {}
boxes = []

def handleUpdate(data):
    id = data["id"]
    angle = data["angle"]
    updater_player = Players[id]
    # рассчитать действия игрока и отослать результаты
    updater_player.SetX(data["x"] if data["x"] else updater_player.X())
    updater_player.SetY(data["y"] if data["y"] else updater_player.Y())
    updater_player.SetAngleView(data["angle"] if data["angle"] else updater_player.angle_view())

    if (data["shot"] == True):
        distance, enemy = hit(updater_player, Players, angle)
        if (enemy):
            if (distance < nearest_wall_shot(([updater_player.X(), updater_player.Y()],
                                             [enemy.X(), enemy.Y()]), boxes)):
                enemy.Decrease_HP(20)
                PlayersEvents[enemy.ID()].append({
                    "shot": True
                })

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
    PlayersEvents[uid] = []
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
def update(data):
    handleUpdate(data)
    if data:
        print(str(data))
    result = {
        "players": []
    }
    for player in Players:
        result["players"].append({
            "x": player.X(),
            "y": player.Y(),
            "angle": player.angle_view(),
            "hp": player.HP()
        })
    result["event"] = PlayersEvents[data["id"]]
    PlayersEvents[data["id"]] = []
    emit('update', result)

if __name__ == '__main__':
    print("Running server! Visit http://127.0.0.1:5000/ for api")
    socketio.run(app, host="0.0.0.0")