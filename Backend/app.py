# Imports
import time

import socketio
from flask import Flask, request, jsonify, json
from flask_socketio import SocketIO
from flask_cors import CORS

# from Database.DP1Database import Database
from Database.DP1Database import Database
from GPIONMCT.Button import Button

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

conn = Database(app=app, user='mct', password='mct', db='Project1', host='localhost', port=3306)
endpoint = '/api/v1'
knop = Button(26)
timer = False
begintijd = ""


def stuurtoestand(pin):
    print(knop.pressed)
    global timer
    global begintijd

    if knop.pressed == True:
        # timer = True
        begintijd = float(time.time())
        # print("Begintijd: %s"%begintijd)

    if knop.pressed == False:
        # timer = False
        eindtijd = float(time.time())
        # print("Eindtijd: %s"%eindtijd)
        verschil = eindtijd - begintijd
        print(verschil)
        verschil = round(verschil, 2)
        print(verschil)
        nieuwe_gebeurtenis = conn.set_data("INSERT INTO historiek (HistoriekID, UserID, Speeltijd) VALUES (NULL, %s, sec_to_time(%s));",[101,verschil])
        socketio.emit("toestand", verschil)


knop.on_action(stuurtoestand)


@app.route(endpoint + '/testconnectie', methods=["GET"])
def testconnectie():
    if request.method == "GET":
        return jsonify(message='geconnecteerd')


@socketio.on("connect")
def connecting():
    socketio.emit("connected")
    print("Connection with client established")

    # randomdata = conn.get_data("select * from users")
    # print(randomdata)
    # socketio.emit("datatest",randomdata)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
