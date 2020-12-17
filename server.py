from main import *
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Timer
from constants import *
import json
import uuid

Players = {}
PlayersEvents = {}
boxes

def handleUpdate(data):
    id = data["id"]
    angle = data["angle"]
    updater_player = Players[id]
    # рассчитать действия игрока и отослать результаты
    updater_player.SetX(data.get("x", updater_player.X()))
    updater_player.SetY(data.get("y", updater_player.X()))
    updater_player.SetAngleView(data.get("angle", updater_player.AngleView()))

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
    data = json.loads(data)
    Players[uid] = Player(uuid,
        data.get("x", 0), 
        data.get("y", 0),
        INITIAL_HP,
        data.get("angle_view", 0.0))
    PlayersEvents[uid] = []
    active_users.add(uid)
    emit('uid', {
        "uid": uid
    })

@socketio.on('stub')
def stub(data):
    print(data)
    emit('stub', json.loads(data))

@socketio.on('update')
def update(data):
    data = json.loads(data)
    handleUpdate(data)
    if data:
        print(str(data), type(data))
    result = {
        "players": []
    }
    for uid, player in Players.items():
        result["players"].append({
            "id": uid,
            "x": player.X(),
            "y": player.Y(),
            "angle": player.AngleView(),
            "hp": player.HP(),
            "id": player.ID()
        })
    result["event"] = PlayersEvents[data["id"]]
    print(str(result))
    PlayersEvents[data["id"]] = []
    emit('update', result)

if __name__ == '__main__':
    print("Running server! Visit http://127.0.0.1:5000/ for api")
    socketio.run(app, host="0.0.0.0")